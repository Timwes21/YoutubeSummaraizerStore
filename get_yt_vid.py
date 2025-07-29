from langchain_core.documents import Document
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
import os
load_dotenv()

video_url = "https://youtu.be/HWRZRfmrxRc?si=_3ie0n8PfD-S8-HK"

# def get_id(url: str):
#     url.split

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username=os.environ["PROXY_USERNAME"],
        proxy_password=os.environ["PROXY_PASSWORD"],
    )
)




def get_id(video_url):
    i = video_url.index("?")
    video_url: str = video_url[:i]
    video_url: list = list(video_url)
    video_url.reverse()
    i = video_url.index("/")
    id = video_url[:i]
    id.reverse()
    id = "".join(id)
    return id


def collect_text(FetchedTranscripts):
    return " ".join([FetchedTranscriptSnippets.text for FetchedTranscriptSnippets in FetchedTranscripts])









def get_video_info(url):
    loader = YoutubeLoaderDL.from_youtube_url(
        url, add_video_info=True
    )
    doc: list[Document] = loader.load()
    video_details = doc[0].metadata
    return video_details["title"], video_details["author"]


def get_script(url: str):
    id = YoutubeLoader.extract_video_id(url)
    info = ytt_api.fetch(id)
    text = collect_text(info)
    return text

# def get_script(url: str):
#     loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
#     return loader.load()






