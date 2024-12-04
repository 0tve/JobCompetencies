import json

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

@app.get('/')
async def hello_world():
    return {'text': 'hello world'}

@app.get('/maps')
async def get_maps():
    
    with open('data/maps.json', encoding='utf-8') as f:
        maps = json.load(f)
        
    return maps