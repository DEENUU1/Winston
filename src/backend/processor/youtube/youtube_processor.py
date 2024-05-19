from .youtube_transcription import YoutubeTranscription
from ai.data_loader import split_raw_text
from ai.rag import save_to_pinecone


def process_youtube_video(url: str, language: str = "English") -> str:
    youtube = YoutubeTranscription(url)

    transcription = youtube.get_transcription(language)

    documents = split_raw_text(transcription)

    for document in documents:
        file_metadata = f"{document.metadata.get('source')}:{document.metadata.get('page')}"

        document.metadata["file_source_page"] = file_metadata
        document.metadata["url"] = url
    save_to_pinecone(documents)

    return url
