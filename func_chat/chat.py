from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
import uvicorn
from chat.run import run_chat
from chat.args import parse_args

app = FastAPI()
templates = Jinja2Templates(directory='./')

@app.get("/chat/")
def get_query_form(request: Request):
    return templates.TemplateResponse('query_form.html', context={'request': request})

@app.post("/chat/")
def input_query(query:str = Form(...)):
    args = parse_args()
    args.query = query
    answer = run_chat(args)
    return {"Question": query, "Answer": answer}

if __name__ == '__main__':
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)