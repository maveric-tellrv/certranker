from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, root_validator
from typing import Dict, Any,List
from fastapi.middleware.cors import CORSMiddleware
from bge import ranker
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define a Pydantic model for the request body
# class Doc(BaseModel):
#     query: str
#     prompt: List[Dict[str,Any]]

class Doc(BaseModel):
    query: str
    prompt: List[Dict[str, Any]]

    @root_validator(pre=True)
    def convert_fetch_doc(cls, values):
        if 'prompt' in values and isinstance(values['prompt'], dict):
            fetch_doc = values['prompt']
            # Convert prompt from dictionary to a list with a single dictionary
            values['prompt'] = [fetch_doc]
        return values

async def preprocess_item(item: Doc) -> Doc:
    # Convert prompt from dictionary to a list with a single dictionary
    if isinstance(item.prompt, dict):
        item.prompt = [item.prompt]
    return item
    

# Route for handling POST requests
@app.post("/rankprompt/")
async def create_item(item: Doc = Depends(preprocess_item)):
    # You can perform any necessary processing/validation here
    # For demonstration purposes, let's just return the received item
    # data = json.loads(item)
    print("\n ***********\n")
    print([item.query],item.prompt)
    similarity = ranker(item.query,item.prompt)
    return similarity


@app.get("/rank/")
async def read_items():
    return {"message": "CERT ReRankers "}