from openai import OpenAI
from pydantic import BaseModel
import streamlit as st
import re
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

class DayOutput(BaseModel):
    response: str
    thoughts: str

class AI_Player():
    def __init__(self, name: str = None, prompt: str = "None"):
        super().__init__()
        self.name = name
        self.client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        self.round_thoughts = []
        self.prompt = prompt

    def respond(self, messages):
        round_chatlog = [
                {"role": "user", "content": m["content"]}
                for m in messages
            ]
        system_messages = [
            {"role": "system", "content": f"Your name in the conversation is {self.name}. Respond to the most recent chats and do not include the *{self.name}: * in your responses. Check the chat logs and maintain continuity."},
            {"role": "system", "content": f"Specific instructions: {self.prompt}."},
            {"role": "system", "content": f"For the output format, the 'response' correspond to your response to the conversation and it must be a string. If you wish to not respond or listen more, put the string 'pass'"},
            {"role": "system", "content": f"For the output format, the 'thoughts' correspond to your thoughts about the conversation and it must be a string. If you dont have any special thoughts about it, put the string 'none'"}
            ] 
        response = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=system_messages + round_chatlog,
            response_format=DayOutput,
        )
        text = str(response.choices[0].message.parsed.response)
        print(str(response.choices[0].message.parsed.thoughts))
        message = re.sub(r'^[^:]+: ', '', text)
        return message