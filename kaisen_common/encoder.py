import vapoursynth as vs
from vardautomation import (
    X265Encoder, QAACEncoder, RunnerConfig, SelfRunner, FileInfo, Mux, make_comps,
    VideoStream, AudioStream, EztrimCutter, FFmpegAudioExtracter, JAPANESE
)

class Encoder:
    runner: SelfRunner

    def __init__(self, file: FileInfo, clip: vs.VideoNode, ED: int = None) -> None:
        self.file = file
        self.clip = clip
        assert self.file.a_src

        if ED:
            self.file.trims_or_dfs = [
                (self.file.trims_or_dfs[0], ED), 
                (ED+2152, ED+2157), 
                (ED, ED+2152), 
                (ED+2157, self.file.trims_or_dfs[-1])
            ]

        self.v_encoder = X265Encoder('../kaisen_common/settings')
        self.a_extracter = FFmpegAudioExtracter(self.file, track_in=1, track_out=1)
        self.a_cutters = EztrimCutter(self.file, track=1)
        self.a_encoders = QAACEncoder(self.file, track=1)

    def run(self) -> None:
        assert self.file.a_enc_cut

        muxer = Mux(
            self.file,
            streams=(
                VideoStream(self.file.name_clip_output, '1080p BD x265 [dedsec]', JAPANESE),
                AudioStream(self.file.a_enc_cut.format(track_number=1), 'AAC 2.0', JAPANESE),
                None
            )
        )

        config = RunnerConfig(
            self.v_encoder, None,
            self.a_extracter, self.a_cutters, self.a_encoders,
            muxer
        )

        self.runner = SelfRunner(self.clip, self.file, config)
        self.runner.run()

    def clean(self):
        self.runner.do_cleanup()

    def compare(self):
        make_comps(
            clips = dict(
                src = self.file.clip_cut,
                flt = self.clip,
                enc = vs.core.ffms2.Source(self.file.name_file_final.to_str())
            ),
            num = 10,
            path = f'../_comps/{self.file.name}',
            collection_name = f'[Kaizoku] {self.file.name}',
            force_bt709 = True,
            slowpics = True,
            public = False
        )
