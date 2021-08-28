import os
import vapoursynth as vs
from typing import Union
from lvsfunc.misc import source
from vardautomation import FileInfo, make_comps

core = vs.core

def generate_comparison(src: FileInfo, enc: Union[os.PathLike[str], str], flt: vs.VideoNode) -> None:
    make_comps(
        clips= {
            'source': src.clip_cut,
            'filtered': flt,
            'encode': source(str(enc))
        },
        collection_name = f'[Kaizoku] {src.name} Test Encode',
        path = f'../_comps/{src.name}', 
        slowpics=True,
    )
