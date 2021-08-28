import os
from vardautomation import FileInfo, PresetFLAC, PresetBD

BDMV = os.path.dirname(__file__)

OP1  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])
ED1  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00006.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])
OP2  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])
ED2  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00018.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])

OP1B = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00010.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])
OP1C = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_2/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])
OP1D = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetFLAC])

OP1E = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetFLAC]) # TODO create this
