import certifi
import requests
from pytube import YouTube
from pytube.request import stream

session = requests.Session()
session.verify = certifi.where()


# Patch pytube to use the configured session
def _patched_get(url, headers, timeout):
    response = session.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.content


stream.get = _patched_get


def download_youtube_video(url, output_path='.'):
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=output_path)
        print(f"Downloaded: {yt.title}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=h02ti0Bl6zk'
    output_path = 'data/'
    download_youtube_video(youtube_url, output_path)
