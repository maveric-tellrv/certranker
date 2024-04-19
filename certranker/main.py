from fastapi import FastAPI, HTTPException,Depends,Request # type: ignore
from pydantic import BaseModel, root_validator # type: ignore
from typing import Dict, Any,List
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from bge import ranker
from testtag import testtag,serialized_data
from testtag import gittag,tcsearch
import json
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI app instance
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



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
    logging.info("Handling /rankprompt/ request...")
    logging.info(f"Received item: {item}")
    similarity = ranker(item.query,item.prompt)
    return {"similarity":similarity}


@app.get("/")
async def read_items():
    logging.info("Handling / request...")
    return {"message": "CERT ReRankers ","version":1.0,"contact":"rovyas@redhat.com"}

class jiraInput(BaseModel):
    jiraid: str

@app.post("/jira/")
async def process_query(jiraid: jiraInput):
    # Print the query parameter and the list of items
    logging.info("Handling POST /jira/ request...")
    logging.info(f"Received jira_id: {jiraid}")

    tests = testtag(jiraid.jiraid)
    # serialized_tests = {str(key): value for key, value in tests.items()}
    # Return a response indicating success
    return (serialized_data(tests))

# Define route for handling GET requests
@app.get("/jira/")
async def process_query_get(jiraid: str):
    logging.info("Handling GET /jira/ request...")
    logging.info(f"Received jira_id: {jiraid}")
    tests = await testtag(jiraid)
    # serialized_tests = {str(key): value for key, value in tests.items()}
    return (serialized_data(tests))

@app.get("/gitlabpr/")
async def process_query(project_id: str,mr_iid: str):

    logging.info("Handling /gitlabpr/ request...")
    logging.info(f"Received project_id: {project_id}, mr_iid: {mr_iid}")

    # headers = {"Authorization": f"Bearer {access_token}"}
    tests =  await gittag(project_id,mr_iid)
    # serialized_tests = {str(key): value for key, value in tests.items()}
    # # Return a response indicating success
    return (serialized_data(tests))



# Your Pydantic model for the request body
class GitlabPRInput(BaseModel):
    project_id: str
    mr_iid: str

@app.post("/gitlabpr/")
async def process_query(GitlabPRInput:GitlabPRInput):

    logging.info("Handling POST /gitlabpr/ request...")
    logging.info(f"Received project_id: {GitlabPRInput.project_id}, mr_iid: {GitlabPRInput.mr_iid}")
    tests =  await gittag(GitlabPRInput.project_id,GitlabPRInput.mr_iid)
    # # Return a response indicating success
    return (serialized_data(tests))


class TestCaseInput(BaseModel):
    testcase: str

@app.post("/testcase/")
async def tcsearch_query(testcase:TestCaseInput):
    
    logging.info("Handling POST /testcase/ request...")
    logging.info(f"Received testcase: {testcase}")
    tc = await tcsearch(testcase.testcase)
    # serialized_tests = {str(key): value for key, value in tc.items()}
    # Return a response indicating success
    return (serialized_data(tc))


async def tc_search(testcase: str):
    # Simulate some asynchronous task, e.g., making an API call
    await asyncio.sleep(1)
    return f"Result for {testcase}"

@app.get("/testcase/")
async def tcsearch_query_get(testcase: str):
    
    logging.info("Handling GET /testcase/ request...")
    logging.info(f"Received testcase: {testcase}")
    tc = await tcsearch(testcase) #tcsearch return a dictionay of testcase:similarity_score
    return (serialized_data(tc)) #searlized the dictionary to be print




if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)