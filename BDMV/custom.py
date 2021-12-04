import os
import lvsfunc as lvf
import kagefunc as kgf
import vardefunc as vdf
from vardautomation import FileInfo

import vapoursynth as vs
core = vs.core

BDMV = os.path.dirname(__file__)
OP1D = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24))
EP13 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00002.m2ts', (24, None))
MASK = fr'{BDMV}/masks/OP1E.png'

def recreate_OP1E():
    src_nc = OP1D.clip_cut
    src_ep = EP13.clip_cut[6954:6954+src_nc.num_frames]
    op = lvf.rfs(src_nc, src_ep, [(2048, 2156)])

    mask = vdf.dcm(op, op[0:src_nc.num_frames-1], src_nc, 0, thr=248, prefilter=True)
    merge = core.std.MaskedMerge(op, src_nc, mask[2075])
    op = lvf.rfs(op, merge, [(2048, 2092)])

    pause = src_ep.std.FreezeFrames(2111, src_ep.num_frames-1, 2111)
    fade = kgf.crossfade(pause[0:2159], core.std.BlankClip(pause), 32)[0:src_nc.num_frames]
    merge = core.std.MaskedMerge(op, fade, mask[2155].std.Minimum().std.Minimum())
    op = lvf.rfs(op, merge, [(2112, 2156)])

    pause = op.std.FreezeFrames(2121, op.num_frames-1, 2121)
    fade = kgf.crossfade(pause[0:2159], core.std.BlankClip(pause), 32)[0:src_nc.num_frames]
    merge = core.std.MaskedMerge(op, fade, mask[2155].std.Minimum().std.Minimum())
    op = lvf.rfs(op, merge, [(2112, 2156)])

    mask_img = core.imwri.Read(MASK).resize.Point(format=fade.format.id, matrix_s="709")
    mask = core.std.Binarize(mask_img, 128).std.Maximum().std.Deflate()
    return core.std.MaskedMerge(fade, op, mask, [0,1,2])

    # i have no idea what i did here
