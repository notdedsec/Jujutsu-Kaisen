from typing import List, Tuple

from vapoursynth import VideoNode
from vardautomation import FileInfo

from vstools import replace_ranges, depth, get_depth, core
from vardefunc import diff_creditless_mask
from vsmasktools import squaremask
from kagefunc import crossfade
from awsmfunc import bbmod


def shift_ed(file: FileInfo, ED: int):
    trims = file.trims_or_dfs

    if not trims:
        return

    if not isinstance(trims[0], int):
        return

    if not isinstance(trims[-1], int) and trims[-1] is not None:
        return

    ED += trims[0]
    trims = [
        (trims[0], ED+10),
        (ED+2152, ED+2157),
        (ED+10, ED+2152),
        (ED+2157, trims[-1])
    ]

    file.trims_or_dfs = trims


def frame_mask(clip: VideoNode, position_x: int, position_y: int, offset_x: int, offset_y: int, frame_width: int, frame_height: int) -> VideoNode:
    mask_a = squaremask(clip, position_x, position_y, offset_x, offset_y)
    mask_b = squaremask(clip, position_x - 2 * frame_width, position_y - 2 * frame_height, offset_x + frame_width, offset_y + frame_height)
    return core.std.Expr([mask_a, mask_b], 'x y -')


def blank_mask(clip: VideoNode) -> VideoNode:
    mask = core.std.BlankClip(clip).std.Invert()
    return core.std.ShufflePlanes(mask, 0, 1)


def letterbox_fix(clip: VideoNode, src: VideoNode, height: int, ranges: List[Tuple[int, int]], offset: int = 1) -> VideoNode:
    src = depth(src, get_depth(clip))
    mask_a = squaremask(clip, clip.width, offset, 0, height)
    mask_b = squaremask(clip, clip.width, offset, 0, clip.height - height - offset)
    mask = core.std.Expr([mask_a, mask_b], 'x y max')
    merge = core.std.MaskedMerge(clip, src, mask)
    crop = merge.std.Crop(top=height, bottom=height)
    bb = bbmod(crop, top=offset, bottom=offset, blur=500)
    fixed = bb.std.AddBorders(top=height, bottom=height)
    return replace_ranges(clip, fixed, ranges)


def recreate_OP1E(EP13: FileInfo, OP1D: FileInfo, OP1E_MASK: FileInfo) -> VideoNode:
    src_nc = OP1D.clip_cut
    src_ep = EP13.clip_cut[6954:6954+src_nc.num_frames]
    op = replace_ranges(src_nc, src_ep, [(2048, 2156)])

    mask = diff_creditless_mask(op, op[0:src_nc.num_frames-1], src_nc, 0, thr=248, prefilter=True)
    merge = core.std.MaskedMerge(op, src_nc, mask[2075])
    op = replace_ranges(op, merge, [(2048, 2092)])

    pause = src_ep.std.FreezeFrames(2111, src_ep.num_frames-1, 2111)
    fade = crossfade(pause[0:2159], core.std.BlankClip(pause), 32)[0:src_nc.num_frames]
    merge = core.std.MaskedMerge(op, fade, mask[2155].std.Minimum().std.Minimum())
    op = replace_ranges(op, merge, [(2112, 2156)])

    pause = op.std.FreezeFrames(2121, op.num_frames-1, 2121)
    fade = crossfade(pause[0:2159], core.std.BlankClip(pause), 32)[0:src_nc.num_frames]
    merge = core.std.MaskedMerge(op, fade, mask[2155].std.Minimum().std.Minimum())
    op = replace_ranges(op, merge, [(2112, 2156)])

    mask_img = core.imwri.Read(OP1E_MASK.path.to_str()).resize.Point(format=fade.format.id, matrix=1)
    mask = core.std.Binarize(mask_img, 128).std.Maximum().std.Deflate().std.Inflate()
    return core.std.MaskedMerge(fade, op, mask, [0, 1, 2])

