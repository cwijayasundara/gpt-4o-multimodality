import base64
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

model = ChatOpenAI(model="gpt-4o", temperature=0)

parser = StrOutputParser()

system_template = "You are a helpful assistant. Help me with my math homework!"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

chain = prompt_template | model | parser

# simple
response = chain.invoke({"text": "Hello! Could you solve 2+2?"})
print(response)

# image from local file

IMAGE_PATH = "../data/triangle.png"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image(IMAGE_PATH)

human_message = HumanMessage(
    content=[
        {"type": "text", "text": "What's the area of the triangle?"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
    ]
)

messages = [
    SystemMessage(content="You are a helpful assistant that responds in Markdown. Help me with my math homework!"),
    human_message,
]

response = model.invoke(messages)
print(parser.invoke(response))

#  image from URL

url = "https://upload.wikimedia.org/wikipedia/commons/e/e2/The_Algebra_of_Mohammed_Ben_Musa_-_page_82b.png"

human_message = HumanMessage(
    content=[
        {"type": "text", "text": "What's the area of the triangle?"},
        {"type": "image_url", "image_url": {"url": url}}
    ]
)

messages = [
    SystemMessage(content="You are a helpful assistant that responds in Markdown. Help me with my math homework!"),
    human_message,
]

response = model.invoke(messages)
print(parser.invoke(response))




