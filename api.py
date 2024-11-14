from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    'http://localhost:3000'
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
@app.get('/routes')
async def get_routes():
    return {
        "endpoints": [
            "/hello",
            "/hellos"
        ]
    }
@app.get('/hello')
async def hello_world():
    return {'text': 'hello world'}

@app.get('/hellos')
async def hello_world():
    return {'text': 'hellos world'}