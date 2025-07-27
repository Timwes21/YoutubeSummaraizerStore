from langchain_core.documents import Document
from langchain_community.document_loaders import YoutubeLoader
from langchain_yt_dlp.youtube_loader import YoutubeLoaderDL



def get_video_info(url):
    loader = YoutubeLoaderDL.from_youtube_url(
        url, add_video_info=True
    )
    doc: list[Document] = loader.load()
    video_details = doc[0].metadata
    return video_details["title"], video_details["author"]


def get_script(url: str):
    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
    return loader.load()
