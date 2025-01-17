import re

from ekstep_data_pipelines.audio_transcription.transcription_sanitizers import (
    BaseTranscriptionSanitizer,
)
from ekstep_data_pipelines.audio_transcription.transcription_sanitizers.audio_transcription_errors import (
    TranscriptionSanitizationError,
)
from ekstep_data_pipelines.common.utils import get_logger

LOGGER = get_logger("UrduTranscriptionSanitizer")


class UrduSanitizer(BaseTranscriptionSanitizer):
    VALID_CHARS = "[ ء-آؤئ-بت-غف-قل-نؤٹپچڈڑژکگںھہیے-ۓ]+"
    PUNCTUATION = "!\"#%&'()*+,./;<=>?@[\\]^_`{|}~।"

    @staticmethod
    def get_instance(**kwargs):
        return UrduSanitizer()

    def __init__(self, *args, **kwargs):
        pass

    def sanitize(self, transcription):
        LOGGER.info("Sanitizing transcription:%s", transcription)
        transcription = transcription.strip()

        transcription = self.replace_bad_char(transcription)

        transcription = transcription.strip()

        if len(transcription) == 0:
            raise TranscriptionSanitizationError("transcription is empty")

        if self.shouldReject(transcription):
            raise TranscriptionSanitizationError(
                "transcription has char which is not in  ء-آؤئ-بت-غف-قل-نؤٹپچڈڑژکگںھہیے-ۓ"
            )

        return transcription

    def shouldReject(self, transcription):
        rejected_string = re.sub(
            pattern=UrduSanitizer.VALID_CHARS, repl="", string=transcription
        )

        if len(rejected_string.strip()) > 0:
            return True

        return False

    def replace_bad_char(self, transcription):

        LOGGER.info("replace panctuation if present ")

        if "-" in transcription:
            transcription = transcription.replace("-", " ")

        table = str.maketrans(dict.fromkeys(UrduSanitizer.PUNCTUATION))
        return transcription.translate(table)
