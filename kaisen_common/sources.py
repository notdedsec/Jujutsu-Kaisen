from vardautomation import FileInfo, PresetAAC, PresetBD
from .custom import recreate_OP1E

BDMV = '../BDMV'

# Episodes

E01 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E02 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E03 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00004.m2ts', (26, -27),  preset=[PresetBD, PresetAAC])

E04 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_2/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E05 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_2/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E06 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_2/BDMV/STREAM/00004.m2ts', (27, -24),  preset=[PresetBD, PresetAAC])

E07 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E08 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00003.m2ts', (27, None), preset=[PresetBD, PresetAAC])
E09 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00004.m2ts', (26, -25),  preset=[PresetBD, PresetAAC])

E10 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_4/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E11 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_4/BDMV/STREAM/00003.m2ts', (25, None), preset=[PresetBD, PresetAAC])
E12 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_4/BDMV/STREAM/00004.m2ts', (27, -25),  preset=[PresetBD, PresetAAC])

E13 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E14 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E15 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00004.m2ts', (26, -27),  preset=[PresetBD, PresetAAC])

E16 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_6/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E17 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_6/BDMV/STREAM/00003.m2ts', (26, None), preset=[PresetBD, PresetAAC])
E18 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_6/BDMV/STREAM/00004.m2ts', (26, -24),  preset=[PresetBD, PresetAAC])

E19 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_7/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E20 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_7/BDMV/STREAM/00003.m2ts', (27, None), preset=[PresetBD, PresetAAC])
E21 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_7/BDMV/STREAM/00004.m2ts', (27, -27),  preset=[PresetBD, PresetAAC])

E22 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_8/BDMV/STREAM/00002.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E23 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_8/BDMV/STREAM/00003.m2ts', (24, None), preset=[PresetBD, PresetAAC])
E24 = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_8/BDMV/STREAM/00004.m2ts', (26, -25),  preset=[PresetBD, PresetAAC])

# Masks

OP1E_MASK = FileInfo(fr'{BDMV}/masks/OP1E.png')
E21A_MASK = FileInfo(fr'{BDMV}/masks/E21A.png')
LETTERBOX_MASK = FileInfo(fr'{BDMV}/masks/LETTERBOX.png')

# Bonus

OP1  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
ED1  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00006.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP2  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
ED2  = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_5/BDMV/STREAM/00018.m2ts', (0, -24), preset=[PresetBD, PresetAAC])

OP1B = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_1/BDMV/STREAM/00010.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1C = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_2/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1D = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])

OP1E = FileInfo(fr'{BDMV}/JUJUTSUKAISEN_3/BDMV/STREAM/00005.m2ts', (0, -24), preset=[PresetBD, PresetAAC])
OP1E.clip_cut = recreate_OP1E(E13, OP1D, OP1E_MASK)

