from typing import List
from mistralai.client import MistralClient
import numpy as np
import os
import requests
import faiss
import os
from datetime import datetime


from mistral import client, run_mistral

INDEXES = {}
CHUNK_TO_ID = {}
ID_TO_CHUNK = {}

EMB_SHAPE = 1024
CHUNK_SIZE = 32
K_SEARCH = 16

def split_text_into_chunks(text: str, chunk_size: int = CHUNK_SIZE):
    chunks = text.split(". ")
    chids = []
    for chunk in chunks:
        chid = len(CHUNK_TO_ID)
        CHUNK_TO_ID[chunk] = chid
        ID_TO_CHUNK[chid] = chunk
        chids.append(chid)

    print(f"split into {len(chunks)} chunks")
    return chunks, chids


def get_text_embedding(chunk: str):
    embeddings_batch_response = client.embeddings(
          model="mistral-embed",
          input=chunk
      )
    emb = embeddings_batch_response.data[0].embedding
    text_embedding = np.array([emb])

    return text_embedding


def get_index(username: str):
    if username in INDEXES:
        ind = INDEXES[username]
    else:
        ind = faiss.IndexFlatL2(EMB_SHAPE)

    return ind


def add_embeddings(username: str, chids: List[int], emb: np.ndarray):
    ind = get_index(username)
    print(emb.shape)
    ind.add(emb)
    INDEXES[username] = ind

def search_similar_chunks(username: str, question: str):
    ind = get_index(username)
    question_embeddings = np.array([get_text_embedding(question)])
    D, I = ind.search(question_embeddings[0], k=K_SEARCH)  # distance, index
    print(D, I)
    retrieved_chunk = [ID_TO_CHUNK[chid] for chid in I.tolist()[0] if chid >= 0]
    print(f"found chunks in docs {retrieved_chunk}")
    return retrieved_chunk


def get_current_dt():
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


def prepare_data():
    users = os.listdir("data/")
    for user in users:
        user_dir = f"data/{user}/"
        for doc in os.listdir(user_dir):
            doc_path = user_dir + doc
            with open(doc_path, "r") as f:
                doc_text = f.read()
                doc_chunks, doc_chids = split_text_into_chunks(doc_text)
                doc_embs = np.vstack([get_text_embedding(chunk) for chunk in doc_chunks])
                add_embeddings(user, doc_chids, doc_embs)

def rag_question(username: str, question: str):


    similars = search_similar_chunks(username, question)
    retrieved_chunk  = " ".join(similars)

    prompt = f"""
    Username: {username}
    Current date: {get_current_dt()}
    Context information is below.
    ---------------------
    {retrieved_chunk}
    ---------------------
    Given the context information and not prior knowledge, answer the query.
    Query: {question}
    Answer:
    """

    answer = run_mistral(prompt)
    print(answer)

    return answer


prepare_data()

if __name__ == "__main__":
    rag_question("oleg", question = "Can I drink Vodka today or why not?")
    rag_question("oleg", question = "what drugs do I need to drink today?")
    rag_question("nick", question = "Can I drink Vodka today or why not?")
    rag_question("nick", question = "what drugs do I need to drink today?")