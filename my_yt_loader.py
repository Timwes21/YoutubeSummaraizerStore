from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain_core.documents import Document

from dotenv import load_dotenv
import os
from youtube_transcript_api.proxies import WebshareProxyConfig
load_dotenv()



proxy_config=WebshareProxyConfig(
    proxy_username=os.environ["PROXY_USERNAME"],
    proxy_password=os.environ["PROXY_PASSWORD"],
)

video_url = "https://youtu.be/HWRZRfmrxRc?si=_3ie0n8PfD-S8-HK"

class UpdatedYoutubeLoader(YoutubeLoader):
    def load(self, proxy) -> list[Document]:
        """Load YouTube transcripts into `Document` objects."""
        try:
            from youtube_transcript_api import (
                FetchedTranscript,
                NoTranscriptFound,
                TranscriptsDisabled,
                YouTubeTranscriptApi,
            )
        except ImportError:
            raise ImportError(
                'Could not import "youtube_transcript_api" Python package. '
                "Please install it with `pip install youtube-transcript-api`."
            )

        if self.add_video_info:
            # Get more video meta info
            # Such as title, description, thumbnail url, publish_date
            video_info = self._get_video_info()
            self._metadata.update(video_info)

        try:
            ytt_api = YouTubeTranscriptApi(proxy_config=proxy)
            transcript_list = ytt_api.list(self.video_id)
        except TranscriptsDisabled:
            return []

        try:
            transcript = transcript_list.find_transcript(self.language)
        except NoTranscriptFound:
            transcript = transcript_list.find_transcript(["en"])

        if self.translation is not None:
            transcript = transcript.translate(self.translation)
        transcript_object = transcript.fetch()
        if isinstance(transcript_object, FetchedTranscript):
            transcript_pieces = [
                {
                    "text": snippet.text,
                    "start": snippet.start,
                    "duration": snippet.duration,
                }
                for snippet in transcript_object.snippets
            ]
        else:
            transcript_pieces: list[dict[str, any]] = transcript_object  # type: ignore[no-redef]

        if self.transcript_format == TranscriptFormat.TEXT:
            transcript = " ".join(
                map(
                    lambda transcript_piece: transcript_piece["text"].strip(" "),
                    transcript_pieces,
                )
            )
            return [Document(page_content=transcript, metadata=self._metadata)]
        elif self.transcript_format == TranscriptFormat.LINES:
            return list(
                map(
                    lambda transcript_piece: Document(
                        page_content=transcript_piece["text"].strip(" "),
                        metadata=dict(
                            filter(
                                lambda item: item[0] != "text", transcript_piece.items()
                            )
                        ),
                    ),
                    transcript_pieces,
                )
            )
        elif self.transcript_format == TranscriptFormat.CHUNKS:
            return list(self._get_transcript_chunks(transcript_pieces))

        else:
            raise ValueError("Unknown transcript format.")
