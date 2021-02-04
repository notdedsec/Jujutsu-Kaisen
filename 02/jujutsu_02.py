#!C:/KaizokuEncoder/python
import os
import acsuite
import subprocess
import vapoursynth as vs

ed = 32008
source =  __file__[:-3]+'.mkv'
premux =  __file__[:-3]+'_premux.mkv'
encode_args = '--crf 16 --preset veryslow --qcomp 0.8 --aq-mode 3 --aq-strength 0.9 --psy-rd 0.85:0.0 --keyint 280 \
    --ref 16 --bframes 16 --rc-lookahead 72 --me tesa --merange 32 --subme 10 --output-depth 10 --deblock -2:-2 \
    --fps 24000/1001 --colormatrix bt709 --colorprim bt709 --transfer bt709 --no-dct-decimate --no-fast-pskip'

script    = source[:-3]+'vpy'
video_out = source[:-3]+'avc'
audio_out = source[:-3]+'aac'
tempfile  = source[:-3]+'_temp.aac'

demux_cmd = ['ffmpeg', '-hide_banner', '-loglevel', '16', '-i', source, '-map', '0:a:0', '-c', 'copy', tempfile]
subprocess.run(demux_cmd)

if ed:
    clip = vs.core.lsmas.LWLibavSource(source)
    trim = [(0, ed), (ed+2152, ed+2157), (ed, ed+2152), (ed+2157, None)]
    acsuite.eztrim(clip, trim, tempfile, audio_out, quiet=True)
    os.remove(tempfile)
    os.remove(source+'.lwi')
else:
    os.rename(tempfile, audio_out)

filter_process = subprocess.Popen(['vspipe', '--y4m', script, '-'], stdout=subprocess.PIPE)
encode_process = subprocess.Popen(['x264'] + encode_args.split() + ['--demuxer', 'y4m', '-o', video_out, '-'], stdin=filter_process.stdout)
filter_process.stdout.close()
encode_process.communicate()

premux_cmd = ['mkvmerge', '-o', premux, video_out, audio_out]
subprocess.run(premux_cmd)
os.remove(video_out)
os.remove(audio_out)
