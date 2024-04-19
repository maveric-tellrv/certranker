from FlagEmbedding import BGEM3FlagModel # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore


def bge():

    bge = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation
    return bge

def minilm():
   
    minilm = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return minilm



