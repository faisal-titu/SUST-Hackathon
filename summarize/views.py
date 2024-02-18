from django.shortcuts import render, redirect

# Create your views here.
import hashlib
from pytube import YouTube
import whisper
import os
from django.http import JsonResponse
import openai
from openai import OpenAI
from dotenv import load_dotenv



def download_video(url):
    yt = YouTube(url)
    hash_file = hashlib.md5()
    hash_file.update(yt.title.encode())
    file_name = f'{hash_file.hexdigest()}.mp4'
    yt.streams.first().download("", file_name)

    return {
        "file_name": file_name,
        "title": yt.title
    }
def split_text(text):
    max_chunk_size = 2048
    chunks = []
    current_chunk = ""
    for sentence in text.split("."):
        if len(current_chunk) + len(sentence) < max_chunk_size:
            current_chunk += sentence + "."
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "."
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks





model_name = "base.en"
model = whisper.load_model(model_name)

def transcribe(url):
    video = download_video(url)
    result = model.transcribe(video["file_name"])
    
    os.remove(video["file_name"])

    segments = []
    for item in result["segments"]:
        segments.append(format_item(item))

    return {
        "title": video["title"],
        "segments": segments
    }
def format_item(item):
    return {
        "time": item["start"],
        "text": item["text"]
    }

def index(request):
    with open("/media/faisal/New Volume/competition/data_extractor/summarize/templates/summarize/index.html", "r") as f:
        index_content = f.read()
    return render(request, '/media/faisal/New Volume/competition/data_extractor/summarize/templates/summarize/index.html', {'index_content': index_content})

def api(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        data = transcribe(url)
        
        text_to_summarize = ''.join([segment['text'] for segment in data['segments']])

        # Summarize the concatenated text
        summarized_data = summarize(text_to_summarize)

        return render(request, 'summarize/index.html', {"summarized_data": summarized_data})
    return JsonResponse({"error": "Method not allowed"}, status=405)


client = OpenAI(api_key="openai_api_key")

def summarize(t):
 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
            "role": "system",
            "content": "Summarize content you are provided with for a second-grade student."
            },
            {
            "role": "user",
            "content": t
            },
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1
        )

    summarized_text = response.choices[0].message.content.strip()
    return summarized_text
