# # news/views.py
# from django.shortcuts import render, redirect
# from .fetch_videos import fetch_videos
# from summarize.views import *

# channel_results = {}  # To store fetched videos

# def news_videos(request):
#     # Replace 'CNN' and 'Al Jazeera English' with the respective YouTube channel IDs
#     channel_results = fetch_videos("Bangladesh TV English News Everyday", "UCglFyFTOF2jTkqHFqi-xN5g")
#     # channel_results.update(fetch_videos("BBC News", "UC16niRr50-MSBwiO3YDb3RA"))
#     # channel_results.update(fetch_videos("CNN", "UCupvZG-5ko_eiXAupbDfxWw"))
#     # channel_results.update(fetch_videos("The Guardian", "UCHpw8xwDNhU9gdohEcJu4aA"))
#     # channel_results.update(fetch_videos("Al Jazeera English", "UCNye-wNBqNL5ZzHSJj3l8Bg"))

#     print("\nChannel Results:", channel_results)  # Print to terminal for verification

#     # Call video_summarize function and pass channel_results as an argument
#     summarized_data_list = video_summarize(channel_results)

#     return render(request, 'news/videos.html', {'channel_results': channel_results, 'summarized_data_list': summarized_data_list})

# def video_summarize(channel_results):
#     summarized_data_list = []  # To store summarized data for all videos
#     print("Channel Results:", channel_results)

#     for channel, videos in channel_results.items():
#         for video in videos:
#             url = video['Video URL']
#             print(f"Processing video: {video['Title']}")

#             try:
#                 data = transcribe(url)
#                 print(f"Transcription data: {data}")

#                 text_to_summarize = ''.join([segment['text'] for segment in data['segments']])
#                 print(f"Text to Summarize: {text_to_summarize}")

#                 summarized_data = summarize(text_to_summarize)
#                 print(f"Summarized Data: {summarized_data}")

#                 summarized_data_list.append(summarized_data)
#                 print(f"Successfully summarized video: {video['Title']}")
#             except Exception as e:
#                 print(f"Error processing video {video['Title']}: {str(e)}")

#     print("Summarized Data List:", summarized_data_list)
#     return summarized_data_list





# news/views.py
from django.shortcuts import render
from .fetch_videos import *
from summarize.views import *
import json



def video_summarize(request):
    # Set the path for the local file
    local_file_path = "summarized_data.json"

    # Check if the local file exists
    if os.path.exists(local_file_path):
        # If the file exists, read the data from the file
        with open(local_file_path, 'r') as file:
            summarized_data_list = json.load(file)
    else:
        # If the file doesn't exist, perform the summarization operation
        summarized_data_list = []
        channel_results = {
            "BBC News": [
                {"Title": "Ukraine’s struggle to find new men for front line | BBC News", "Video ID": "UCglFyFTOF2jTkqHFqi-xN5g", "Video URL": "http://www.youtube.com/watch?v=K-v1LNKRLmQ"},
                {"Title": "King Charles diagnosed with cancer, Buckingham Palace says | BBC News", "Video ID": "UCglFyFTOF2jTkqHFqi-xN5g", "Video URL": "http://www.youtube.com/watch?v=igYmSzom8YE"},
                {"Title": "King meets Prince Harry as he “steps back” from duties for cancer treatment | BBC News", "Video ID": "UCglFyFTOF2jTkqHFqi-xN5g", "Video URL": "http://www.youtube.com/watch?v=_aRvw-GzHJc"}
            ],
            "CNN News": [
                {"Title": "Michelle Obama is trending and you won't believe why", "Video ID": "UCglFyFTOF2jTkqHFqi-xN5g", "Video URL": "http://www.youtube.com/watch?v=CAxp8JYxhx4"},
                {"Title": "Ex-Trump WH lawyer says this part of Trump ruling is ‘very, very important’", "Video ID": "UCglFyFTOF2jTkqHFqi-xN5g", "Video URL": "http://www.youtube.com/watch?v=Tp4xaM6Cj6A"},
                {"Title": "Trump Lawyer INSTANTLY CUT OFF by CNN host, CRUSHED by Brutal fact-check", "Video ID": "UCglFyFTOF2jTkqHFqi-xN5g", "Video URL": "http://www.youtube.com/watch?v=2k0juGvJuH4"}
            ]
        }

        for channel, videos in channel_results.items():
            for video in videos:
                url = video['Video URL']
                print(f"Processing video: {video['Title']}")
                try:
                    data = transcribe(url)
                    print(f"Transcription data: {data}")

                    text_to_summarize = ''.join([segment['text'] for segment in data['segments']])
                    print(f"Text to Summarize: {text_to_summarize}")

                    summarized_data = summarize(text_to_summarize)
                    print(f"Summarized Data: {summarized_data}")

                    summarized_data_list.append(summarized_data)
                    print(f"Successfully summarized video: {video['Title']}")
                except Exception as e:
                    print(f"Error processing video {video['Title']}: {str(e)}")

        # Save the summarized data to the local file
        with open(local_file_path, 'w') as file:
            json.dump(summarized_data_list, file)

    print("Summarized Data List:", summarized_data_list)
    return render(request, 'news/videos.html', {'summarized_data_list': summarized_data_list})