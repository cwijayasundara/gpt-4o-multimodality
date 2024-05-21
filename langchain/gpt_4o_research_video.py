import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from util.util import process_video

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0)

parser = StrOutputParser()

VIDEO_PATH = "../data/OpenAI DevDay Keynote Recap.mp4"

base64Frames, audio_path = process_video(VIDEO_PATH, seconds_per_frame=1)

#  summarise the video
human_message = HumanMessage(
    content=[
        "These are the frames from the video.",
        *map(lambda x: {"type": "image_url",
                        "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames)
    ]
)

system_message = SystemMessage(content="You are generating a video summary. Please provide a summary of the video. "
                                       "Respond in Markdown.")
messages = [
    system_message,
    human_message,
]

response = model.invoke(messages)
print("video summery", parser.invoke(response))

# summarise the audio
# Transcribe the audio
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=open(audio_path, "rb"),
)

system_message = SystemMessage(content="""You are generating a transcript summary. Create a summary of the provided
                                          transcription. Respond in Markdown.""")
user_message = HumanMessage([
    {"type": "text", "text": f"The audio transcription is: {transcription.text}"}
])

messages = [
    system_message,
    user_message,
]

response = model.invoke(messages)
print("audio summary", parser.invoke(response))

# Audio + Visual Summary
system_message = SystemMessage(content="""You are generating a video summary. Create a summary of the provided video
                                       and its transcript. Respond in Markdown""")
user_message = HumanMessage([
    "These are the frames from the video.",
    *map(lambda x: {"type": "image_url",
                    "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames),
    {"type": "text", "text": f"The audio transcription is: {transcription.text}"}
])

messages = [
    system_message,
    user_message,
]

response = model.invoke(messages)
print(parser.invoke(response))

