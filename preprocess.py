#!C:/KaizokuEncoder/python
import re
import os
import sys
import math
import datetime
import subprocess
import ass
import subdigest
import vapoursynth as vs

def get_input(args):
    '''
    Function to handle script's arguments.
    '''
    if len(args) == 2:
        return args[1]
    elif len(args) == 1:
        infile = input('Provide the file to be processed: ')
        if os.path.exists(infile):
            return infile
        else:
            sys.exit('Invalid path or file does not exist.')
    else:
        sys.exit('The script accepts only one parameter. Make sure the file name is enclosed in quotes.')

def get_episode_number(infile):
    '''
    Extract episode number from file name.
    '''
    partial = re.search(r"(\b|E|_)([0-9]{1,3})(\b|_|v)", infile).group(0)
    episode = re.search(r"([0-9]{1,3})", partial).group(0)
    return episode.zfill(2)

def parse_properties(properties, ep):
    '''
    Read data from a properties file and return key value pairs in a dict.
    '''
    def insert_vars(expression, variables):
        '''
        Replace variable names with their values in parsed strings.
        ''' 
        inserted = ''
        for token in expression.split('${'):
            if '}' in token:
                name, rest = token.split('}')
                try:
                    inserted += variables[name]+rest
                except:
                    pass #sys.exit(f"Error: Variable '{name}' not defined in properties.")
            else:
                inserted += ' '+token
        inserted = inserted.strip().replace('*', '')
        return inserted

    with open(properties, 'r') as f:
        lines = f.readlines()
    variables = {'episode': ep}
    for line in lines:
        if '=' not in line:
            continue
        key, val = line.split('=')
        variables.update({key.strip(): insert_vars(val.strip(), variables)})
    return variables

def dump_subs(subsfile, subsdata):
    '''
    Exports subsdata to subsfile manually over using dump_file() to avoid the utf-8 encode warning.
    '''
    with open(subsfile, 'w', encoding='utf_8_sig') as f:
        for section in subsdata.sections.values():
            f.write("\n".join(section.dump()))
            f.write("\n\n")

def load_subs(subsfile):
    '''
    Loads up and parses subtitles from subsfile and returns subsdigest object.
    '''
    with open(subsfile, encoding='utf_8_sig') as f:
        subsdata = subdigest.Subtitles(ass.parse(f), subsfile)
    return subsdata

def append(subsfile, text):
    '''
    Appends the given text at the end of subsfile.
    '''
    with open(subsfile, 'a+', encoding='utf_8_sig') as f:
        f.write(text)

def crunchy_unroll(infile, source, ep, styles, res, dialogue, typesets):
    '''
    Cleans up subtitles by combining Crunchyroll's million signs/title styles into a single 'Signs' style.
    Combines Main, Italics, Flashbacks styles under a 'Default' style as well with italics tags if needed.
    Adds autoswapper syntax for common honorifics. Resamples and copies styles from default template file.
    Lastly, splits the subs into _dialogue.ass and _typesets.ass files.
    '''
    # append project garbage cause too lazy to import
    src = os.path.split(source)[-1]
    append(infile, f'\n[Aegisub Project Garbage]\nAudio File: {src}\nVideo File: {src}')
    subs = load_subs(infile)

    # merge all sign styles
    subs.modify_field("style", ".*Ep_Title", "Signs")
    subs.modify_field("style", "^sign.*", "Signs")
    subs.selection_set("text", r"\\fs")
    subs.selection_add("text", r"\\fn")
    subs.selection_add("text", r"\\pos")
    subs.modify_field("style", "^.*", "Signs")
    subs.selection_set("style", ".*_Title")
    subs.remove_selected()

    # merge all italics styles
    subs.selection_set("style", "Italics$")
    subs.modify_field("text", "^", r"{\\i1}")
    subs.modify_field("text", "}{", "")

    # merge all dialogue styles
    subs.selection_add("style", "Main")
    subs.selection_add("style", "Flashback")
    subs.selection_add("style", "Narration")
    subs.modify_field("style", "^.*", "Default")

    # add autoswapper syntax to be edited later
    subs.modify_field("text", "-san", "{**-san}")
    subs.modify_field("text", "-kun", "{**-kun}")
    subs.modify_field("text", "-chan", "{**-chan}")
    subs.modify_field("text", "-sama", "{**-sama}")
    subs.modify_field("text", "-senpai", "{**-senpai}")
    subs.modify_field("text", "-sensei", "{*}{*-sensei}")
    subs.modify_field("text", "Sensei", "{*}{*Sensei}")

    # some terminology changes
    subs.modify_field("text", "Yuuji", "Yuji")
    subs.modify_field("text", "Gojou", "Gojo")
    subs.modify_field("text", "Yuuta", "Yuta")
    subs.modify_field("text", "Jougo", "Jogo")
    subs.modify_field("text", "Getou", "Geto")
    subs.modify_field("text", "Toudou", "Todo")
    subs.modify_field("text", "Shouko", "Shoko")
    subs.modify_field("text", "Chousou", "Choso")
    subs.modify_field("text", "Ryoumen", "Ryomen")

    # nuke \N tags
    subs.modify_field("text", r"\s*{\\i0}\s*\\N\s*{\\i1}\s*", " ")
    subs.modify_field("text", r"\s*\\[Nn]\s*", " ")
    subs.modify_field("text", r"\s*\\[Nn]", " ")
    subs.modify_field("text", r"\\[Nn]\s*", " ")
    subs.modify_field("text", r"\\[Nn]", " ")

    # misc
    subs.modify_field("text", "--", "—")

    # nuke old styles
    subs.use_styles()
    subs.remove_selected()

    # copy new styles
    temp = f'{ep}_temp.ass'
    dump_subs(temp, subs)
    subprocess.run(['python', '-m', 'prass', 'copy-styles', '--from', styles, '--to', temp, '--resolution', res, '-o', temp])
    # idk why resampling messes up CR's TS but we're gonna redo it anyway so /shrug
    
    # export dialogue file
    dialogue_data = load_subs(temp)
    dialogue_data.selection_set("style", "Default").keep_selected()
    dump_subs(dialogue, dialogue_data)

    # export typesets file
    typesets_data = load_subs(temp)
    typesets_data.selection_set("style", "Default").remove_selected().remove_unused_styles()
    dump_subs(typesets, typesets_data)

    os.remove(temp)

def generate_keyframes(source, keyframes):
    '''
    Generates keyframes to be imported in Aegisub for simplifying timing.
    Based on kagefunc's generate_keyframes() with some formatting tweaks.
    '''
    if os.path.exists(keyframes):
        return

    clip = vs.core.ffms2.Source(source)
    clip = vs.core.resize.Bilinear(clip, 640, 360, vs.YUV420P8)
    clip = vs.core.wwxd.WWXD(clip)
    text = '# WWXD log file, using qpfile format\n\n'

    for frame in range(clip.num_frames):
        if clip.get_frame(frame).props['Scenechange'] == 1:
            text += "%d I -1\n" % frame
        if frame % 1000 == 0:
            print(f"Progress: {int(frame/clip.num_frames*100)}%", end="\r")

    os.remove(source+'.ffindex')
    with open(keyframes, 'w') as f:
        f.write(text)

def get_timestamps(dialogue, fps):
    '''
    Reads 'chptr' comments from dialogue subs to find timestamps of OP, ED and Eyecatch.
    Chapters must be named in the following format:
        Opening
        Part B
        Ending
        ...
    Returns a dict of timestamps and frame numbers.
    '''
    op = ec = ed = opsync = ecsync = edsync = None

    with open(dialogue, encoding='utf_8_sig') as f:
        dialogue_data = ass.parse(f)

    for event in dialogue_data.events:
        if not isinstance(event, ass.line.Comment) and not event.name == 'chptr':
            continue
        if 'opening' in event.text.lower():
            opsync = event.start
            op = math.ceil(opsync.total_seconds() * fps)
        if 'ending'  in event.text.lower():
            edsync = event.start
            ed = math.ceil(edsync.total_seconds() * fps)
        if 'part b'  in event.text.lower(): # Part B / Eyecatch 
            ecsync = event.start
            ec = math.ceil(ecsync.total_seconds() * fps)

    return {'op': op, 'ec': ec, 'ed': ed, 'opsync': opsync, 'ecsync': ecsync, 'edsync': edsync}

def get_title(typesets, ep):
    '''
    Tries to grab the title from the typesets file. Returns a generic title if none found.
    '''
    title = None
    typesets_data = load_subs(typesets)
    print('Episode title is set to: ', end='')

    for event in typesets_data.events:
        if '\\pos' in event.text and 'Episode' in event.text:
            title = f'{ep}. {event.text.split(":", 1)[1].strip()}'
            title = re.sub(r"\s*\{.*\}\s*", " ", title)
            break 

    if not title:
        title = f'Episode {ep}'

    print(title)
    return title

def write_vpy(vpy_base, vpy_file, source, ts):
    '''
    Reads the base script and timestamp data, removes all comments, adds frame numbers and input files 
    for the current episode and saves the vapoursynth script in the episode folder.
    '''
    with open(vpy_base, 'r') as f:
        vpy_script = f.readlines()

    for line in vpy_script:
        if line.strip().startswith('# '):
            vpy_script.remove(line)
        elif line.startswith('op ='):
            vpy_script[vpy_script.index(line)] = f'op = {ts["op"]}\n'
        elif line.startswith('ec ='):
            vpy_script[vpy_script.index(line)] = f'ec = {ts["ec"]}\n'
        elif line.startswith('ed ='):
            vpy_script[vpy_script.index(line)] = f'ed = {ts["ed"]}\n'
        elif line.startswith('source ='):
            vpy_script[vpy_script.index(line)] = f'source = os.path.join(os.getcwd(), "{os.path.split(source)[-1]}")\n'

    with open(vpy_file, 'w') as f:
        f.writelines(vpy_script)

def write_enc(enc_base, enc_file, ts):
    '''
    Reads the base script and timestamp data, removes all comments, adds frame numbers
    for the current episode and saves the encode script in the episode folder.
    '''
    with open(enc_base, 'r') as f:
        enc_script = f.readlines()

    for line in enc_script:
        if line.strip().startswith('# '):
            enc_script.remove(line)
        elif line.startswith('ed ='):
            enc_script[enc_script.index(line)] = f'ed = {ts["ed"]}\n'

    with open(enc_file, 'w') as f:
        f.writelines(enc_script)

def main():
    '''
    Master function to handle all processing.
    '''
    # read input and prepare work folder
    infile = get_input(sys.argv)
    ep = episode = get_episode_number(infile)
    if not os.path.exists(ep):
        os.makedirs(os.path.join(ep, 'fonts'))

    # parsing properties and into a variables dict
    v = parse_properties('sub.properties', ep)

    # inserting values of variables in the parsed strings, fallback to defaults if undefined in sub.properties
    
    # pre-existing variables for subkt
    source   = v['source']   if 'source'   in v.keys() else f'{ep}/{v["showkey"]}_{ep}.mkv'
    premux   = v['premux']   if 'premux'   in v.keys() else f'{ep}/{v["showkey"]}_{ep}_encode.mkv'
    dialogue = v['dialogue'] if 'dialogue' in v.keys() else f'{ep}/{v["showkey"]}_{ep}_subs_dialogue.ass'
    typesets = v['typesets'] if 'typesets' in v.keys() else f'{ep}/{v["showkey"]}_{ep}_subs_typesets.ass'

    # new variables for this script
    vpy_file = v['vpy_file'] if 'vpy_file' in v.keys() else f'{ep}/{v["showkey"]}_{ep}.vpy'
    enc_file = v['enc_file'] if 'enc_file' in v.keys() else f'{ep}/{v["showkey"]}_{ep}.py'
    keyframes=v['keyframes'] if 'enc_file' in v.keys() else f'{ep}/{v["showkey"]}_{ep}_keyframes.txt'

    # mandatory variables, exiting if undefined
    styles   = v['styles']   if 'styles'   in v.keys() else sys.exit("Error: Variable 'styles' not defined in properties.")
    vpy_base = v['vpy_base'] if 'vpy_base' in v.keys() else sys.exit("Error: Variable 'vpy_base' not defined in properties.")
    enc_base = v['enc_base'] if 'enc_base' in v.keys() else sys.exit("Error: Variable 'enc_base' not defined in properties.")

    # some more optional variables
    fps = int(v['fps']) if 'fps' in v.keys() else 23.976
    res = v['res'] if 'res' in v.keys() else '1080p'

    if infile.endswith('.ass'):
        print('Processing subtitles.')
        crunchy_unroll(infile, source, ep, styles, res, dialogue, typesets)
        sys.exit('Done')

    subprocess.run(['mkvextract', '-q', 'tracks', infile, f'2:{infile}.ass'])
    os.rename(infile, source)
    infile += '.ass'
    
    print('Processing subtitles.')
    crunchy_unroll(infile, source, ep, styles, res, dialogue, typesets)

    print('Generating keyframes.')
    print('While this gets done, edit the dialogue track and mark the chapter timestamps.')
    generate_keyframes(source, keyframes)

    if input('Done with the timestamps? [y/n] : ').lower() == 'n':
        sys.exit()

    print('Great! Parsing timestamp data.')
    ts = get_timestamps(dialogue, fps)
    properties  = f'\n{ep}.title='+'${show} - '+f'{get_title(typesets, ep)}\n'
    properties += f'{ep}.opsync={ts["opsync"]}\n{ep}.edsync={ts["edsync"]}\n'
    properties += f'{ep}.ecsync={ts["ecsync"] - datetime.timedelta(seconds=5)}\n'
    properties += f'{ep}.pic=None\n'

    print('Setting up base vapoursynth script.')
    write_enc(enc_base, enc_file, ts)

    print('Setting up base encode script.')
    write_vpy(vpy_base, vpy_file, source, ts)

    print('Updating sub.properties and Aegisub Project Garbage.') # this time just the keyframes
    append(dialogue, f'\n[Aegisub Project Garbage]\nKeyframes File: {os.path.split(keyframes)[-1]}')
    append(typesets, f'\n[Aegisub Project Garbage]\nKeyframes File: {os.path.split(keyframes)[-1]}')
    append('sub.properties', properties)

    print('Done.\n')

if __name__ == "__main__":
    main()
