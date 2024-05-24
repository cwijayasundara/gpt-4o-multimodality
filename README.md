This repo contains sample code to use Gpt-4o for multimodel use cases. I also got this integrated with Langchain (https://www.langchain.com/) which is a popular framework to build Gen AI applications.

GPT-4o ("o" for "omni") is designed to handle a combination of text, audio, and video inputs, and can generate outputs in text, audio, and image formats

Currently, the API supports {text, image} inputs only, with {text} outputs, the same modalities as gpt-4-turbo. Additional modalities, including audio, will be introduced soon.

Getting started:

- Clone this repo to your local machine / VM : git clone https://github.com/cwijayasundara/gpt-4o-multimodality.git
- Make sure you have Python 3.11 or above installed on your machine / VM
- Create a .env file with the below key & value. Use your OpenAI key here!
-   OPENAI_API_KEY='sk-********'
- More information about getting an OpenAI key and setting up a .env can be found here. https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key
- Install the dependencies required for the project by executing pip install -r requirements.txt from the root
- You would need two python packages for video processing - opencv-python and moviepy. These are provided in the requirements.txt
- These require ffmpeg, so make sure to install this beforehand. Depending on your OS, you may need to run brew install ffmpeg or sudo apt install ffmpeg
- After the dev set up is done just cd to the langchain dir and then python gpt_4o_research_images.py to execute the image processor.
- Enjoy!!
