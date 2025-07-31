from langchain_core.documents import Document
from langchain_community.document_loaders import YoutubeLoader
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL
from youtube_transcript_api.proxies import WebshareProxyConfig
from dotenv import load_dotenv
from my_yt_loader import UpdatedYoutubeLoader
import asyncio
import json
import os
import requests
import httpx
load_dotenv()

video_url = "https://youtu.be/HWRZRfmrxRc?si=_3ie0n8PfD-S8-HK"

# def get_id(url: str):
#     url.split

proxy_config=WebshareProxyConfig(
    proxy_username=os.environ["PROXY_USERNAME"],
    proxy_password=os.environ["PROXY_PASSWORD"],
)

yt_api_key = os.environ["YT_API_KEY"]



async def get_video_info(url):
    print(url)
    video_id = UpdatedYoutubeLoader.extract_video_id(url)
    print(video_id)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={yt_api_key}"
    async with httpx.AsyncClient() as e:
        info = await e.get(url)
        info_parsed = info.json()
        info = info_parsed["items"][0]["snippet"]
        return info["title"], info["channelTitle"]


def get_script(url: str):
    try:
        print("here in the beginning")
        loader = UpdatedYoutubeLoader.from_youtube_url(
            url, add_video_info=False
        )
        print("getting transcripts")
        i = loader.load(proxy_config)
        print("got transcript")
        transcript = i[0].page_content
        print(len(transcript))
        
        # print(transcript)
        return transcript
    except Exception as e:
        print(e)
    



