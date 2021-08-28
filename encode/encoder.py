import vapoursynth as vs
from .util import generate_comparison
from vardautomation import (
    X265Encoder, QAACEncoder, RunnerConfig, SelfRunner, FileInfo, Mux,
    VideoStream, AudioStream, EztrimCutter, FfmpegAudioExtracter, JAPANESE
)

core = vs.core

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

        self.v_encoder = X265Encoder('../encode/settings')
        self.a_extracter = FfmpegAudioExtracter(self.file, track_in=1, track_out=1)
        self.a_cutters = EztrimCutter(self.file, track=1)
        self.a_encoders = QAACEncoder(self.file, track=1)
    
    def run(self) -> None:
        assert self.file.a_enc_cut

        muxer = Mux(
            self.file,
            streams=(
                VideoStream(self.file.name_clip_output, '1080p BD x265 [dedsec]', JAPANESE),
                AudioStream(self.file.a_enc_cut, 'AAC 2.0', JAPANESE),
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
        generate_comparison(self.file, self.file.name_file_final.to_str(), self.clip)
