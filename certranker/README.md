
 # CertTestRanker

CertTestRanker is a FastAPI-based service designed for ranking test cases, fetching relevant Testcases, and processing queries related to Jira issues and GitLab merge requests.

## Overview

This project provides a RESTful API with various endpoints to perform different tasks related to test case ranking and querying. The API endpoints include:

- `POST /rankprompt/`: Rank prompts based on similarity.
- `POST /jira/`: Process Jira issues and return related test cases.
- `GET /jira/`: Get test cases related to a specific Jira issue.
- `GET /gitlabpr/`: Get test cases related to a GitLab merge request.
- `POST /gitlabpr/`: Process GitLab merge requests and return related test cases.
- `POST /testcase/`: Search for test cases based on a given input.
- `GET /testcase/`: Get similarity scores for test cases.

## Installation

To set up the CertTestRanker service, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/maveric-tellrv/certranker.git
2. Install the dependencies:
   pip install -r requirements.txt
3. Run the service:
    uvicorn main:app --host 0.0.0.0 --port 8000
```

## Usage
    Rank Test Prompts

    Endpoint: POST /rankprompt/
    Description: Rank test prompts based on similarity.
    Request Body:
    ``` {
     "query": "Your query string",
    "prompt": [
        {
        "key1": "value1",
        "key2": "value2",
         ...
        }
    ]
    }
```

Response :
    {
  "similarity": "Similarity score"
}


 Process Jira Issues

    Endpoint: POST /jira/
    Description: Process Jira issues and return related test cases.
    Request Body:

    json

    {
      "jiraid": "Jira issue ID"
    }

    Response: Test cases related to the specified Jira issue.

Process GitLab Merge Requests

    Endpoint: POST /gitlabpr/
    Description: Process GitLab merge requests and return related test cases.
    Request Body:

    json

    {
      "project_id": "Project ID",
      "mr_iid": "Merge Request IID"
    }

    Response: Test cases related to the specified GitLab merge request.

Search for Test Cases

    Endpoint: POST /testcase/
    Description: Search for test cases based on a given input.
    Request Body:

    json

    {
      "testcase": "Test case name or description"
    }

    Response: Test cases matching the input.

Get Similarity Scores for Test Cases

    Endpoint: GET /testcase/
    Description: Get similarity scores for test cases.
    Query Parameter:
        testcase: Test case name or description.
    Response: Similarity scores for test cases.

## Contact

For inquiries or support, please contact slack #maveric-tellrv.


## Pre-Requisite 

Create a config.py in the same dir with 
```
 
    jira_server=config.jira_server
    jira_token=config.jira_token
    connection=config.connection
    collection_name=config.collection_name
    access_token = config.git_access_token

```


This README provides an overview of the CertTestRanker project, including installation instructions, usage details for each endpoint, and contact information. Adjustments can be made based on specific requirements or additional features of the project. Let me know if you need further modifications or assistance!

## Example:
```
1. /rankprompt

 curl --location 'http://127.0.0.1:8000/rankprompt/' \
  --header 'Content-Type: application/json' \
  --data ' {
      "query":  "Who was the father of Mary Ball Washington?",
      "prompt":[
      {
          "question": "Who lived longer, Muhammad Ali or Alan Turing?",
          "answer": "\nAre follow up questions needed here: Yes.\nFollow up: How old was Muhammad Ali when he died?\nIntermediate answer: Muhammad Ali was 74 years old when he died.\nFollow up: How old was Alan Turing when he died?\nIntermediate   answer: Alan Turing was 41 years old when he died.\nSo the final answer is: Muhammad Ali\n"
      },
      {
          "question": "When was the founder of craigslist born?",
          "answer": "\nAre follow up questions needed here: Yes.\nFollow up: Who was the founder of craigslist?\nIntermediate answer: Craigslist was founded by Craig Newmark.\nFollow up: When was Craig Newmark born?\nIntermediate answer: Craig Newmark   was born on December 6, 1952.\nSo the final answer is: December 6, 1952\n"
      },
      {
          "question": "Who was the maternal grandfather of George Washington?",
          "answer": "\nAre follow up questions needed here: Yes.\nFollow up: Who was the mother of George Washington?\nIntermediate answer: The mother of George Washington was Mary Ball Washington.\nFollow up: Who was the father of Mary Ball   Washington?\nIntermediate answer: The father of Mary Ball Washington was Joseph Ball.\nSo the final answer is: Joseph Ball\n"
      },
      {
          "question": "Are both the directors of Jaws and Casino Royale from the same country?",
          "answer": "\nAre follow up questions needed here: Yes.\nFollow up: Who is the director of Jaws?\nIntermediate Answer: The director of Jaws is Steven Spielberg.\nFollow up: Where is Steven Spielberg from?\nIntermediate Answer: The United   States.\nFollow up: Who is the director of Casino Royale?\nIntermediate Answer: The director of Casino Royale is Martin Campbell.\nFollow up: Where is Martin Campbell from?\nIntermediate Answer: New Zealand.\nSo the final answer is: No\n"
      },{
          "question": "Are both the directors of Jaws and Casino Royale from the same country?"
      }]}'
OUTPUT:
  {
    "similarity": [
        [
            "Who was the maternal grandfather of George Washington?",
            "\nAre follow up questions needed here: Yes.\nFollow up: Who was the mother of George Washington?\nIntermediate answer: The mother of George Washington was Mary Ball Washington.\nFollow up: Who was the father of Mary Ball Washington?\nIntermediate answer: The father of Mary Ball Washington was Joseph Ball.\nSo the final answer is: Joseph Ball\n",
            0.7287863492965698
        ],
        [
            "When was the founder of craigslist born?",
            "\nAre follow up questions needed here: Yes.\nFollow up: Who was the founder of craigslist?\nIntermediate answer: Craigslist was founded by Craig Newmark.\nFollow up: When was Craig Newmark born?\nIntermediate answer: Craig Newmark was born on December 6, 1952.\nSo the final answer is: December 6, 1952\n",
            0.3634181022644043
        ],
        [
            "Who lived longer, Muhammad Ali or Alan Turing?",
            "\nAre follow up questions needed here: Yes.\nFollow up: How old was Muhammad Ali when he died?\nIntermediate answer: Muhammad Ali was 74 years old when he died.\nFollow up: How old was Alan Turing when he died?\nIntermediate answer: Alan Turing was 41 years old when he died.\nSo the final answer is: Muhammad Ali\n",
            0.33534735441207886
        ],
        [
            "Are both the directors of Jaws and Casino Royale from the same country?",
            "\nAre follow up questions needed here: Yes.\nFollow up: Who is the director of Jaws?\nIntermediate Answer: The director of Jaws is Steven Spielberg.\nFollow up: Where is Steven Spielberg from?\nIntermediate Answer: The United States.\nFollow up: Who is the director of Casino Royale?\nIntermediate Answer: The director of Casino Royale is Martin Campbell.\nFollow up: Where is Martin Campbell from?\nIntermediate Answer: New Zealand.\nSo the final answer is: No\n",
            0.33021965622901917
        ],
        [
            "Are both the directors of Jaws and Casino Royale from the same country?",
            null,
            0.3302196264266968
        ]
    ]
}


3. /testcase
    curl --location 'http://127.0.0.1:8000/testcase/' \
  --header 'Content-Type: application/json' \
  --data {
      "testcase": "openstack nuetron test cases"
  }

4. Jira
  curl --location --request GET 'http://localhost:8000/jira/?jira_id=CERTPX-12717' \
  --header 'Content-Type: application/json' \
  --data '{"jira_id": "JIRAID-12717"}' 

5. gitpr
  curl --location 'http://localhost:8000/gitlabpr/?project_id=56673&mr_iid=235' 
