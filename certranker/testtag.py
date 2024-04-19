from jira import JIRA # type: ignore
from FlagEmbedding import BGEM3FlagModel # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
from langchain_cohere import CohereEmbeddings # type: ignore
from langchain_core.documents import Document # type: ignore
from langchain_postgres import PGVector # type: ignore
from gitlabpr import gitexatract
from models import bge,minilm
import config
import asyncio


model = minilm()
bge = bge()

jira_server=config.jira_server
jira_token=config.jira_token
connection=config.connection
collection_name=config.collection_name


def certJira(jiraid,jira_server=jira_server,jira_token=jira_token):

    """ Function returns accepts args as JIRA server and JIra token 
        Returns :summary    
    """
 
    
    jira_object = JIRA(server = jira_server, token_auth = jira_token)
    issues = jira_object.issue(jiraid)
    summary = issues.fields.summary
    # description = issues.fields.description
    # jira_info = summary+description
    # return jira_info
    return summary

async def retieval(query,connection=connection,collection_name=collection_name,model=model):

    vectorstore = PGVector(embeddings=model,
                           collection_name=collection_name,
                           connection=connection,use_jsonb=True,)

    x = vectorstore.similarity_search(query,k=20)
    testcase = [i.page_content for i in x]
    return testcase
    

async def bgeranker(query,listoftest):

    """ Functiona accepts arg1 query string
                        arg2 : List of Test cases
                         Returns relevant testcase ranker 
                         with similarity score in descending order 
    """

    sentences_1 = query
    sentences_2 = listoftest

    embeddings_1 = bge.encode(sentences_1, 
                            batch_size=12, 
                            max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                            )['dense_vecs']
    embeddings_2 = bge.encode(sentences_2)['dense_vecs']
    similarity = embeddings_1 @ embeddings_2.T
    # similarity_list = [round(element * 100, 2) for element in similarity.tolist()]
    # print(similarity)
    # ranked = {k:v for k,v in zip(sentences_2,similarity_list)}
    ranked = {k:v for k,v in zip(sentences_2,similarity.tolist())}
    sorted_dict = dict(sorted(ranked.items(), key=lambda item: item[1], reverse=True))

    return sorted_dict

async def testtag(jiraid):

    """ 
    Function accepts Args as JIRA ID 
    Return relevant Tc
    """
    
    query = certJira(jiraid)
    tc = await retieval(query)
    relevanceTest =await bgeranker(query,tc)
    # serialized_data = {str(key): value for key, value in relevanceTest.items()}

    return (relevanceTest)

async def gittag(project_id,mr_iid):

    query = gitexatract(project_id,mr_iid)
    tc = await retieval(query)
    relevanceTest = await bgeranker(query,tc)
    # serialized_data = {str(key): value for key, value in relevanceTest.items()}

    return (relevanceTest)

async def tcsearch(query):
    
    tc = await retieval(query) #retrival from database
    relevanceTest =  await bgeranker(query,tc) #bge ranker to rank the similarity search

    return (relevanceTest)

def serialized_data(tests):
    # here test is a dictionary object 

    serialized_data = {str(key): value for key, value in tests.items()}
    return serialized_data

    
if __name__ == "__main__":
    
    # Put your code here that you want to execute when this script is run directly
    print("T\n testcase search based on JIRA:\n")
    tests = testtag('xx-12339')
    # Convert dictionary keys to strings
    # serialized_data = {str(key): value for key, value in tests.items()}
    print(tests)