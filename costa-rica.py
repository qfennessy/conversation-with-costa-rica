from pinecone import Pinecone, ServerlessSpec

import os
from dotenv import load_dotenv

from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from operator import itemgetter
import tempfile
import whisper
from pytube import YouTube
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import glob
from langchain_community.document_loaders import TextLoader
from langchain_pinecone import PineconeVectorStore


parser = StrOutputParser()

def create_url_list():
    with open('video-urls.txt', 'r') as file:
        urls = [line.strip() for line in file]
    return urls




def transcribe_video(urls):
    # Let's load the base model. This is not the most accurate
    # model but it's fast.
    whisper_model = whisper.load_model("base")
    
    print("in transcribe_video")
    for url in urls:
        # Let's do this only if we haven't created the transcription file yet.
        transcript_file = f"transcription_{url.split('=')[-1]}.txt"
        if not os.path.exists(transcript_file):
            youtube = YouTube(url)
            audio = youtube.streams.filter(only_audio=True).first()

            with tempfile.TemporaryDirectory() as tmpdir:
                file = audio.download(output_path=tmpdir)
                transcription = whisper_model.transcribe(file, fp16=False)["text"].strip()

                with open(f"transcription_{url.split('=')[-1]}.txt", "w") as file:
                    file.write(transcription)
        print(f"Transcript file {transcript_file} already exists.")

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")

model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4-turbo")

parser = StrOutputParser()
urls = create_url_list()
transcribe_video(urls)


for filename in glob.glob('transcription_*.txt'):
    with open(filename, 'r') as file:
        content = file.read()
        print(content[:100])


transcripts = []
for url in urls:
    transcript_file = f"transcription_{url.split('=')[-1]}.txt"
    print(f"transcript_file: {transcript_file}")
    loader = TextLoader(transcript_file)
    transcripts.append(loader.load())
text_documents = ''.join(transcripts)

print(text_documents)

