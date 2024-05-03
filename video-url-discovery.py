from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

def fetch_travel_videos(api_key: str, query: str, max_results: int = 10) -> list:
    """
    Fetch URLs of top travel videos for a given query on YouTube.

    Args:
        api_key (str): Your API key for the YouTube Data API.
        query (str): The search query (e.g., "Costa Rica travel").
        max_results (int): Maximum number of results to return.

    Returns:
        list: A list of video URLs.

    Raises:
        HttpError: If an error occurs accessing the YouTube API.
    """
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_response = youtube.search().list(
        q=query,
        part='id',
        maxResults=max_results,
        order='relevance',
        type='video'
    ).execute()

    video_urls = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        video_urls.append(f'https://www.youtube.com/watch?v={video_id}')
    
    return video_urls


def read_api_key_from_file(file_path: str = "~/.youtube-api") -> str:
    """
    Read the YouTube Data API key from a file.

    Args:
        file_path (str): The path to the file containing the API key.

    Returns:
        str: The API key.
    """
    file_path = os.path.expanduser(file_path)
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key



# Replace 'YOUR_API_KEY' with your actual YouTube Data API key
if __name__ == '__main__':
    api_key = read_api_key_from_file()

    try:
        videos = fetch_travel_videos(api_key, 'Costa Rica travel 2024',20)
        for url in videos:
            print(url)
    except HttpError as e:
        print(f'An HTTP error occurred: {e.resp.status} {e.content}')
        

videos = fetch_travel_videos(api_key, 'Costa Rica travel')
