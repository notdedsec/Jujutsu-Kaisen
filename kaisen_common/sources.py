import os

from vardautomation import FileInfo, VPath, PresetAAC, PresetBD
from .utils import recreate_OP1E

BDMV = VPath(os.path.dirname(__file__)).parent / 'BDMV'


# Episodes

E01 = FileInfo(BDMV / 'JUJUTSUKAISEN_1/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E02 = FileInfo(BDMV / 'JUJUTSUKAISEN_1/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E03 = FileInfo(BDMV / 'JUJUTSUKAISEN_1/BDMV/STREAM/00004.m2ts', (26, -27),  preset=[PresetBD, PresetAAC])

E04 = FileInfo(BDMV / 'JUJUTSUKAISEN_2/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E05 = FileInfo(BDMV / 'JUJUTSUKAISEN_2/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E06 = FileInfo(BDMV / 'JUJUTSUKAISEN_2/BDMV/STREAM/00004.m2ts', (27, -24),  preset=[PresetBD, PresetAAC])

E07 = FileInfo(BDMV / 'JUJUTSUKAISEN_3/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E08 = FileInfo(BDMV / 'JUJUTSUKAISEN_3/BDMV/STREAM/00003.m2ts', (27, None), preset=[PresetBD, PresetAAC])
E09 = FileInfo(BDMV / 'JUJUTSUKAISEN_3/BDMV/STREAM/00004.m2ts', (26, -25),  preset=[PresetBD, PresetAAC])

E10 = FileInfo(BDMV / 'JUJUTSUKAISEN_4/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E11 = FileInfo(BDMV / 'JUJUTSUKAISEN_4/BDMV/STREAM/00003.m2ts', (25, None), preset=[PresetBD, PresetAAC])
E12 = FileInfo(BDMV / 'JUJUTSUKAISEN_4/BDMV/STREAM/00004.m2ts', (27, -25),  preset=[PresetBD, PresetAAC])

E13 = FileInfo(BDMV / 'JUJUTSUKAISEN_5/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E14 = FileInfo(BDMV / 'JUJUTSUKAISEN_5/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E15 = FileInfo(BDMV / 'JUJUTSUKAISEN_5/BDMV/STREAM/00004.m2ts', (26, -27),  preset=[PresetBD, PresetAAC])

E16 = FileInfo(BDMV / 'JUJUTSUKAISEN_6/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E17 = FileInfo(BDMV / 'JUJUTSUKAISEN_6/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E18 = FileInfo(BDMV / 'JUJUTSUKAISEN_6/BDMV/STREAM/00004.m2ts', (26, -24),  preset=[PresetBD, PresetAAC])

E19 = FileInfo(BDMV / 'JUJUTSUKAISEN_7/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E20 = FileInfo(BDMV / 'JUJUTSUKAISEN_7/BDMV/STREAM/00003.m2ts', (27, None), preset=[PresetBD, PresetAAC])
E21 = FileInfo(BDMV / 'JUJUTSUKAISEN_7/BDMV/STREAM/00004.m2ts', (27, -27),  preset=[PresetBD, PresetAAC])

E22 = FileInfo(BDMV / 'JUJUTSUKAISEN_8/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E23 = FileInfo(BDMV / 'JUJUTSUKAISEN_8/BDMV/STREAM/00003.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E24 = FileInfo(BDMV / 'JUJUTSUKAISEN_8/BDMV/STREAM/00004.m2ts', (26, -25),  preset=[PresetBD, PresetAAC])


# Bonus

OP1  = FileInfo(BDMV / 'JUJUTSUKAISEN_1/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
ED1  = FileInfo(BDMV / 'JUJUTSUKAISEN_1/BDMV/STREAM/00006.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP2  = FileInfo(BDMV / 'JUJUTSUKAISEN_5/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
ED2  = FileInfo(BDMV / 'JUJUTSUKAISEN_5/BDMV/STREAM/00018.m2ts', (0, -24), preset=[PresetBD, PresetAAC])

OP1B = FileInfo(BDMV / 'JUJUTSUKAISEN_1/BDMV/STREAM/00010.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1C = FileInfo(BDMV / 'JUJUTSUKAISEN_2/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1D = FileInfo(BDMV / 'JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1E = FileInfo(BDMV / 'JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])

OP1E_MASK = FileInfo(BDMV / 'masks/OP1E.png')
OP1E.clip_cut = recreate_OP1E(E13, OP1D, OP1E_MASK)

