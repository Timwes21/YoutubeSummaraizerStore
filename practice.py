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


id = get_id(video_url)
print(id)


info = ytt_api.fetch(id)
text = collect_text(info)
print(text)

