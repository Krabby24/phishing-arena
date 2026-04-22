import os
import anthropic
from agents.base_agent import BaseAgent


class ClaudeAgent(BaseAgent):

    def __init__(self, model: str = "claude-sonnet-4-6", instance_id: int = 1):
        super().__init__(name=f"claude-{model}-{instance_id}")
        self.model = model
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def _generate(self, system_prompt: str, user_message: str) -> str:
        return self._call_api(system_prompt, user_message)

    def _call_api(self, system_prompt: str, user_message: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        raw = response.content[0].text
        return raw