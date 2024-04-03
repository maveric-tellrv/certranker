from FlagEmbedding import BGEM3FlagModel
from fastapi.encoders import jsonable_encoder
from collections import namedtuple

model = BGEM3FlagModel('BAAI/bge-m3',  
                       use_fp16=True) # Setting use_fp16 to True speeds up computation with a slight performance degradation


def ranker(toMatch,fetchDoc):

    # Define the named tuple structure
    Document = namedtuple('Document', ['description','answer', 'score'])
    
 
    fetchDoc_list = [d[list(d.keys())[0]] for d in fetchDoc]

    fetchDoc_list_ans = []

    # Iterate over each dictionary in the fetchDoc list
    for d in fetchDoc:
        # Check if the dictionary contains at least two keys
        if len(d) >= 2:
            # Access the second key and append its value to the answers list
            fetchDoc_list_ans.append(d[list(d.keys())[1]])
        else:
            # Handle the case where the dictionary doesn't contain the required key
            fetchDoc_list_ans.append(None)  # or any other appropriate handling

        # fetchDoc_list_ans = [d[list(d.keys())[1]] for d in fetchDoc]
   
    print(f"\n******\n{fetchDoc_list}\n*********\n")
    toMatch_embeddings = model.encode(toMatch, 
                                batch_size=12, 
                                max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
                                )['dense_vecs']
    fetchDoc_embeddings = model.encode(fetchDoc_list)['dense_vecs']
    similarity = toMatch_embeddings @ fetchDoc_embeddings.T
    print(f"SIMILARITY: {similarity}")
    # Convert lists to named tuples
    Document = [Document(description,answer, score) for description,answer, score in zip(fetchDoc_list,fetchDoc_list_ans,similarity.tolist())]
    print(Document)
    sorted_Document = sorted(Document, key=lambda x: x.score,reverse=True)
    json_data = jsonable_encoder(sorted_Document)

    
    return json_data


def getEmbeddings(fetchDoc):

    embeddings = model.encode(fetchDoc)['dense_vecs']


if __name__ == "__main__":
    # Put your code here that you want to execute when this script is run directly
    print("This script is being executed directly")