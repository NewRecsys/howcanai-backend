from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Completion(BaseModel):
    model: str
    prompt: str

@app.post("/v1/chat/completions")
def chat(completion: Completion):
    return {
      "id": "chatcmpl-123",
      "object": "chat.completion",
      "created": 1677652288,
      "choices": [{
        "index": 0,
        "message": {
          "role": "assistant",
          "content": "\n\nHello there, how may I assist you today?",
        },
        "finish_reason": "stop"
      }],
      "usage": {
        "prompt_tokens": 9,
        "completion_tokens": 12,
        "total_tokens": 21
      }
    }
