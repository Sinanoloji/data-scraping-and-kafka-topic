import uvicorn
from fastapi import FastAPI
import json

app = FastAPI()

@app.get("/")
async def data_read():
    file = open("pokemon.json")
    return json.load(file)

if __name__ == "__main__":
    uvicorn.run(app,port=8080)
