import os
from typing import Any, Dict, Tuple, Optional

from vapoursynth import VideoNode
from vardautomation import (
    X265, FFV1, QAACEncoder, RunnerConfig, SelfRunner, FileInfo, MatroskaFile, MediaTrack,
    EztrimCutter, FFmpegAudioExtracter, SlowPicsConf, make_comps, patch, JAPANESE
)

from .utils import shift_ed


class Encoder:
    runner: SelfRunner
    settings = f'{os.path.dirname(__file__)}/settings'


    def __init__(self, file: FileInfo, clip: VideoNode, zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None, shift: Optional[int] = None):
        self.file = file
        self.clip = clip
        self.zones = zones

        if shift:
            shift_ed(self.file, shift)


    def run(self):
        assert self.file.a_enc_cut

        out_mkv = MatroskaFile(
            self.file.name_file_final,
            [
                MediaTrack(self.file.name_clip_output, 'BD 1080p HEVC [dedsec]', JAPANESE),
                MediaTrack(self.file.a_enc_cut.format(track_number=1), 'Japanese 2.0 AAC', JAPANESE)
            ]
        )

        config = RunnerConfig(
            v_encoder = X265(self.settings, zones=self.zones),
            v_lossless_encoder = FFV1(),
            a_extracters = FFmpegAudioExtracter(self.file, track_in=1, track_out=1),
            a_cutters = EztrimCutter(self.file, track=1),
            a_encoders = QAACEncoder(self.file, track=1),
            mkv = out_mkv
        )

        self.runner = SelfRunner(self.clip, self.file, config)
        self.runner.run()


    def run_patch(self, ranges):
        patch(
            encoder = X265(self.settings, zones=self.zones),
            clip = self.clip,
            file = self.file,
            ranges = ranges
        )


    def clean(self):
        # self.runner.work_files.clear()
        self.runner.rename_final_file(f'{self.file.name}_premux.mkv')


    def compare(self):
        return
        make_comps(
            clips = dict(
                src = self.file.clip_cut,
                flt = self.clip,
                enc = FileInfo(self.file.name_file_final).clip
            ),
            slowpics_conf = SlowPicsConf(
                collection_name = f'[Kaizoku] {self.file.name}',
                public=False
            ),
            path = f'{os.path.dirname(__file__)}/../_comps/{self.file.name}',
            num = 10
        )
