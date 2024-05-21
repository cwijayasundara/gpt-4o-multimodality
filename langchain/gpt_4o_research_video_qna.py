import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from util.util import process_video
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

parser = StrOutputParser()

VIDEO_PATH = "../data/OpenAI DevDay Keynote Recap.mp4"

base64Frames, audio_path = process_video(VIDEO_PATH, seconds_per_frame=1)

transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=open(audio_path, "rb"),
)

# video QA
QUESTION = "Question: Why did Sam Altman have an example about raising windows and turning the radio on?"

system_message = SystemMessage(content="""Use the video to answer the provided question. Respond in Markdown.""")

human_message = HumanMessage(
    content=[
        "These are the frames from the video.",
        *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}},
             base64Frames),
        QUESTION
    ]
)

messages = [
    system_message,
    human_message,
]

qa_visual_response = model.invoke(messages)
print("Visual QA:\n" + parser.invoke(qa_visual_response))

# audio QA

# system_message = SystemMessage(content="""Use the transcription to answer the provided question.
#                                           Respond in Markdown.""")
# human_message = HumanMessage(content=[
#     {f"The audio transcription is: {transcription.text}"},
#     QUESTION
# ])
#
# messages = [
#     system_message,
#     human_message,
# ]
#
# qa_audio_response = model.invoke(messages)
# print("Audio QA:\n" + parser.invoke(qa_audio_response))


# video and audio Q&A
system_message = SystemMessage(content="""Use the video and transcription to answer the provided question.""")
human_message = HumanMessage(
    content=[
        "These are the frames from the video.",
        *map(lambda x: {"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}},
             base64Frames),
        f"The audio transcription is: {transcription.text}. \n\n {QUESTION}"
    ]
)

messages = [
    system_message,
    human_message,
]

qa_audio_visual_response = model.invoke(messages)
print("Audio Visual QA:\n" + parser.invoke(qa_audio_visual_response))
