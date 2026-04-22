import os
from openai import OpenAI
from agents.base_agent import BaseAgent


class DeepSeekAgent(BaseAgent):

    def __init__(self, model: str = "deepseek-chat", instance_id: int = 1):
        super().__init__(name=f"deepseek-{model}-{instance_id}")
        self.model = model
        # DeepSeek espone un'API compatibile OpenAI
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )

    def _generate(self, system_prompt: str, user_message: str) -> str:
        return self._call_api(system_prompt, user_message)

    def _call_api(self, system_prompt: str, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content