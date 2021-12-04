import os
from . import custom
from vardautomation import FileInfo, PresetAAC, PresetBD

BDMV = os.path.dirname(__file__)

OP1  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
ED1  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00006.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP2  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
ED2  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00018.m2ts', (0, -24), preset=[PresetBD, PresetAAC])

OP1B = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00010.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1C = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_2/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1D = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])

OP1E = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1E.clip_cut = custom.recreate_OP1E()
