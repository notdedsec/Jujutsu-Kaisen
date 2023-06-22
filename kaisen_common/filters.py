#!C:/KaizokuEncoderV2/python

from typing import List, Dict, Any, Tuple
from vardautomation import FileInfo
from vapoursynth import VideoNode

from vsaa import Nnedi3
from vsaa.antialiasers.eedi3 import Eedi3SR
from vskernels import Bicubic, BicubicDidee
from vsscale import SSIM, descale_detail_mask
from vsdenoise import MVTools, SADMode, Prefilter, ccd
from vstools import replace_ranges, join, core, Matrix
from vsutil import get_w, get_y, get_depth, depth
from havsfunc import FineDehalo, EdgeCleaner
from jvsfunc import retinex_edgemask
from adptvgrnMod import adptvgrnMod
from debandshit import dumb3kdb
from stgfunc import set_output

from .utils import letterbox_fix


class Filter:

    native_res = 844


    def __init__(
        self,
        SRC: FileInfo,
        AA_RANGES: List[Tuple[int, int]] = [],
        CURSED_BANDING_RANGES: List[Tuple[int, int]] = [],
        NO_DENOISE_RANGES: List[Tuple[int, int]] = [],
        RESTORE_MASKS: Dict[Tuple[int, int], VideoNode] = {},
        LETTERBOX_RANGES: Dict[Tuple[int, int], Dict[str, Any]] = {},
    ):

        self.SRC = SRC
        self.AA_RANGES = AA_RANGES
        self.CURSED_BANDING_RANGES = CURSED_BANDING_RANGES
        self.NO_DENOISE_RANGES = NO_DENOISE_RANGES
        self.RESTORE_MASKS = RESTORE_MASKS
        self.LETTERBOX_RANGES = LETTERBOX_RANGES


    def process(self):
        src = depth(self.SRC.clip_cut, 16)
        src_y = get_y(src)

        descaled = Bicubic().descale(src_y, get_w(self.native_res), self.native_res)
        upscaled = Nnedi3(pscrn=1).scale(descaled, descaled.width*2, descaled.height*2)

        eedi3 = Eedi3SR(alpha=0.125, beta=0.25, gamma=80, vthresh0=12, vthresh1=24, vthresh2=4, sclip_aa=True)
        aa = eedi3.aa(upscaled.std.Transpose())
        aa = eedi3.aa(aa.std.Transpose())

        fine_dehalo = FineDehalo(aa, darkstr=0, thlimi=16, thmi=64)
        edge_clean = EdgeCleaner(fine_dehalo, strength=8, smode=1, hot=True)
        dehalo = core.std.Expr([fine_dehalo, edge_clean], 'x y min')

        ssim_downscale = SSIM(sigmoid=True, kernel=BicubicDidee()).scale(dehalo, src.width, src.height)
        retinex_mask = retinex_edgemask(src_y).std.Inflate().std.Maximum().std.Inflate()
        downscaled = core.std.MaskedMerge(src_y, ssim_downscale, retinex_mask)

        bicubic_upscale = Bicubic().scale(descaled, src.width, src.height)
        restore_mask = descale_detail_mask(src_y, bicubic_upscale, thr=0.04, inflate=4, xxpand=(4, 4))
        for mask_range, mask_clip in self.RESTORE_MASKS.items():
            mask_clip = get_y(depth(mask_clip, get_depth(restore_mask)))
            restore_mask = replace_ranges(restore_mask, mask_clip, mask_range)
        restored = core.std.MaskedMerge(downscaled, src_y, restore_mask)

        denoise_y = MVTools.denoise(restored, thSAD=48, block_size=32, overlap=16, prefilter=Prefilter.MINBLUR2, sad_mode=SADMode.SPATIAL.same_recalc)
        denoise_y = denoise_y.ttmpsm.TTempSmooth(maxr=1, thresh=1, mdiff=0, strength=1)
        denoise_y = replace_ranges(denoise_y, restored, self.NO_DENOISE_RANGES)
        denoise_c = ccd(src, thr=4, planes=[1, 2], matrix=Matrix.BT709)
        denoise = join(denoise_y, denoise_c)

        dumb_deband_normal = dumb3kdb(denoise, radius=16, threshold=24, use_neo=True)
        dumb_deband_strong = dumb3kdb(denoise, radius=16, threshold=48, use_neo=True)
        dumb_deband = replace_ranges(dumb_deband_normal, dumb_deband_strong, self.CURSED_BANDING_RANGES)
        deband = core.std.MaskedMerge(dumb_deband, denoise, retinex_mask)

        grain = adptvgrnMod(deband, strength=0.24, luma_scaling=8, sharp=64, grain_chroma=False, static=True)
        final = depth(grain, 10).std.Limiter(16 << 2, [235 << 2, 240 << 2], [0, 1, 2])

        for ranges, params in self.LETTERBOX_RANGES.items():
            params['ranges'] = ranges
            final = letterbox_fix(final, src, **params)

        set_output(src)
        # set_output(upscaled)
        # set_output(aa)
        # set_output(dehalo)
        # set_output(retinex_mask)
        # set_output(downscaled)
        # set_output(restore_mask)
        # set_output(restored)
        # set_output(denoise)
        # set_output(deband)
        set_output(final)

        return final

