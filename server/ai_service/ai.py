import tiktoken
from openai import OpenAI

from conf.config import CONFIG


class AI:
    def __init__(self):
        self.model_name = "gpt-3.5-turbo-0125"
        self.client = OpenAI(
            api_key=CONFIG.openai_token,
        )
        self.token_model = tiktoken.encoding_for_model(self.model_name)

    def chat(self, user_input: str):
        response = self.client.chat.completions.create(
            n=1,
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )
        content = response.choices[0].message.content
        return content
