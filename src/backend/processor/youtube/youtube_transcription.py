from typing import Optional, List, Dict, Any, Tuple
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled


class YoutubeTranscription:
    def __init__(self, url: str):
        self.video_id = self.get_youtube_video_id(url)

    @staticmethod
    def get_youtube_video_id(url: str) -> Optional[str]:
        query = urlparse(url)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]

        return None

    @staticmethod
    def map_languages_to_code(language: str) -> str:
        mapper = {
            "Danish": "da",
            "Czech": "cs",
            "Dutch": "nl",
            "English": "en",
            "German": "de",
            "French": "fr",
            "Italian": "it",
            "Japanese": "ja",
            "Korean": "ko",
            "Polish": "pl",
            "Spanish": "es",
        }
        return mapper[language]

    def fetch_transcription(self, language: str) -> Optional[List[Dict[str, Any]]]:
        text, type_ = None, None
        generated, manually = None, None

        try:
            transcription_list = YouTubeTranscriptApi.list_transcripts(self.video_id)

            if not transcription_list:
                print(f"No audio found for video {self.video_id}")
                return text

            for transcript in transcription_list:
                if language in transcript.language:
                    if transcript.is_generated:
                        generated = transcript
                    else:
                        manually = transcript

            if not generated and not manually:
                lang_code = self.map_languages_to_code(language)

                for transcript in transcription_list:
                    translation_languages = transcript.translation_languages

                    for lang in translation_languages:
                        if language in lang.get("language"):
                            generated = transcript.translate(lang_code)

            if generated and manually:
                text = manually.fetch()

            elif generated:
                text = generated.fetch()

        except TranscriptsDisabled:
            print(f"Transcripts disabled for video {self.video_id}")
            return text

        except Exception as e:
            print(e)
            return text

        return text

    @staticmethod
    def format_text(full_text: List[Dict[str, Any]]) -> str:
        result = ""

        for text in full_text:
            result += text.get("text")

        result.strip().replace("\n", " ")

        return result

    def get_transcription(self, language: str) -> Optional[str]:
        fetched_transcript = self.fetch_transcription(language)

        if fetched_transcript is None:
            print(f"No audio found for video {self.video_id}")
            return None

        print(f"Transcription fetched for video {self.video_id}")
        formatted_text = self.format_text(fetched_transcript)

        print(f"Transcription formatted for video {self.video_id}")

        return formatted_text


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=EXk0IYtSpes"
    yt = YoutubeTranscription(url)
    print(yt.get_transcription("English"))
