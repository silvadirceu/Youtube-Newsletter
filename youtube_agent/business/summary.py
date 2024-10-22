from langflow.load import run_flow_from_json
from youtube_agent.services.config import settings
from youtube_agent import schemas

class BusinessSumary():
    async def summarize_video(self, video: schemas.VideoBase, video_transcription: str) -> str:
        TWEAKS = {
    "ChatInput-wHJjj": {
        "files": "",
        "input_value": video_transcription,
        "sender": "User",
        "sender_name": "User",
        "session_id": "",
        "store_message": True
    },
    "Prompt-OLGmh": {
        "template": "You are an AI helping a user in resuming Youtube videos for him, so he will decide if should watch it or not. \nAnswer only in Portuguese and format you message in Markdown format.\nYou will recieve the video name and the \nvideo's transcription and need to answer with a paragraph about it.\n\nUse the following format:\n*Vídeo:* [Video name]\n*Canal:* [Channel name]\n*Resumo:* [Explaining what this video is about]\n\n\nVideo name: {video_name}\nChannel name: {channel_name}\nVideo Transcript: {user_input}\n\nAnswer (in Portuguese): ",
        "user_input": "",
        "video_name": "",
        "channel_name": ""
    },
    "ChatOutput-fxhSA": {
        "data_template": "{text}",
        "input_value": "",
        "sender": "Machine",
        "sender_name": "AI",
        "session_id": "",
        "store_message": True
    },
    "GroqModel-aj41X": {
        "groq_api_base": "https://api.groq.com",
        "groq_api_key": settings.GROQ_API_KEY,
        "input_value": "",
        "max_tokens": None,
        "model_name": "llama-3.1-8b-instant",
        "n": None,
        "stream": False,
        "system_message": "",
        "temperature": 0.1
    },
    "TextInput-lngfO": {
        "input_value": video.title
    },
    "OpenAIModel-Q4AFX": {
        "api_key": settings.OPENAI_API_KEY,
        "input_value": "",
        "json_mode": False,
        "max_tokens": None,
        "model_kwargs": {},
        "model_name": "gpt-4o-mini",
        "openai_api_base": "",
        "output_schema": {},
        "seed": 1,
        "stream": False,
        "system_message": "",
        "temperature": 0.1
    },
    "TextInput-D563R": {
        "input_value": video.channelTitle
    }
    }

        result = run_flow_from_json(flow="youtube_agent/services/youtuber_summarizer.json",
                                    input_value="message",
                                    fallback_to_env_vars=True, # False by default
                                    tweaks=TWEAKS)
        return result[0].outputs[0].results["message"].data["text"]


summarizer = BusinessSumary()