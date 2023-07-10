from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Completion(BaseModel):
    model: str | None = None
    prompt: str | None = None

@app.post("/v1/chat/completions")
def chat(completion: Completion):
    return {
      "id": "cmpl-uqkvlQyYK7bGYrRHQ0eXlWi7",
      "object": "text_completion",
      "created": 1589478378,
      "model": "text-davinci-003",
      "choices": [
        {
          "text": "이것은 howcan.ai의 답변입니다.",
          "index": 0,
          "logprobs": None,
          "finish_reason": "length"
        }
      ],
      "usage": {
        "prompt_tokens": 5,
        "completion_tokens": 7,
        "total_tokens": 12
    }
}
