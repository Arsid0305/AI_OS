import os
import time
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI()


def call_model(messages, temperature=0.2, max_tokens=4000):
    start = time.time()

    try:
        print(">>> MODEL CALL START")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=30,
        )

        latency = round(time.time() - start, 2)
        usage = response.usage

        print(">>> MODEL CALL DONE:", latency)

        return {
            "content": response.choices[0].message.content,
            "latency": latency,
            "tokens_prompt": usage.prompt_tokens if usage else 0,
            "tokens_completion": usage.completion_tokens if usage else 0,
            "model": MODEL,
        }

    except Exception as e:
        print("⛔ MODEL ERROR:", e)
        return None


class OpenAIEngine:

    def call(self, messages, temperature=0.2):
        return call_model(messages, temperature=temperature)