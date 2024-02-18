# # news/fetch_videos.py
# from googleapiclient.discovery import build
# # from .views import channel_results
# from dotenv import load_dotenv
# import os

# load_dotenv()

# def fetch_videos(channel_name, channel_id):
    
#     api_key = os.getenv('YOUTUBE_API_KEY')
#     # api_key = 'YOUTUBE_API_KEY'  # Replace with your actual API key
#     youtube = build('youtube', 'v3', developerKey=api_key)

#     channel_results = {}  # Initialize the dictionary
#     playlist_response = youtube.channels().list(part='contentDetails', id=channel_id).execute()

#     if 'items' in playlist_response and playlist_response['items']:
#         uploads_playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

#         videos_response = youtube.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=5).execute()

#         videos_list = []
#         for video in videos_response.get('items', []):
#             video_data = {
#                 "Title": video['snippet']['title'],
#                 "Video ID": video['snippet']['resourceId']['videoId'],
#                 "Video URL": f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}"
#             }
#             videos_list.append(video_data)

#         channel_results[channel_name] = videos_list



# Import the necessary modules
from googleapiclient.discovery import build

# Replace 'YOUR_API_KEY' with the actual API key you obtained
api_key = 'AIzaSyCTlr07kewtZhcFttD-UM55LFtYtYePWOE'
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to fetch videos and add to the dictionary
# news/fetch_videos.py
# news/fetch_videos.py
def fetch_videos(channel_name, channel_id):
    print(f"\nFetching videos for {channel_name}:\n")
    playlist_response = youtube.channels().list(part='contentDetails', id=channel_id).execute()

    channel_results = {}  # Initialize channel_results here

    if 'items' in playlist_response:
        if playlist_response['items']:
            uploads_playlist_id = playlist_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

            videos_response = youtube.playlistItems().list(part='snippet', playlistId=uploads_playlist_id, maxResults=1).execute()

            channel_results[channel_name] = []
            for video in videos_response['items']:
                video_data = {
                    "Title": video['snippet']['title'],
                    "Video_ID": video['snippet']['resourceId']['videoId'],
                    "Video_URL": f"https://www.youtube.com/watch?v={video['snippet']['resourceId']['videoId']}"
                }
                print(video_data)  # Add this line to debug
                channel_results[channel_name].append(video_data)

    print(f"\nFinal Videos for {channel_name}: {channel_results[channel_name]}")
    return channel_results  # Return the channel_results dictionary
