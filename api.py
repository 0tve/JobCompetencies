from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def hello_world(request: Request):
    return templates.TemplateResponse(request, 'index.html', {'message': 'Hello!!!!!'})