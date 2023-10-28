
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
import chromadb
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings
from chromadb.utils import embedding_functions
from typing import List
import uuid

class VectorStore:
    def __init__(self):
        # self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.default_ef = embedding_functions.DefaultEmbeddingFunction()
        # self.client = chromadb.PersistentClient(Settings(chroma_db_impl="duckdb+parquet",
        #                             persist_directory="db/"
        #                         ))
        self.client=chromadb.PersistentClient(path="db/")
        
        
        

    

    def add_question(self,query,sql,plot_params,data_description,collection_name):
        collection = self.client.get_or_create_collection(name=collection_name,embedding_function=self.default_ef)
        collection.add(
        documents = [query],
        metadatas = [{"sql":sql,'plot_params':plot_params,'data_description':data_description}],
        ids = [str(uuid.uuid4())]
    )   
        print("Query added to Vector DB")


    def add_suggestion(self,query,collection_name):
        collection = self.client.get_or_create_collection(name=collection_name,embedding_function=self.default_ef)
        collection.add(
        documents = [query],
        ids = [str(uuid.uuid4())]
    )   
        print("Suggestion added to Vector DB")


    def query_vdb(self, query, n,collection_name):
    # Fetching results based on query
        collection = self.client.get_or_create_collection(name=collection_name,embedding_function=self.default_ef)
        results = collection.query(
            query_texts=[query],
            n_results=n)

        # Return empty dict if results are empty
        if not results['documents'][0] or not results['distances'][0] or not results['metadatas'][0]:
            return {}

        # Getting required data from results
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        # Filtering based on value of n and distance threshold
        output_dict = {}
   
        if n == 1:
            if distances[0] < 0.1:
                output_dict[documents[0]] = metadatas[0]  # Assign the entire metadata dictionary
        else:
            for doc, meta, dist in zip(documents, metadatas, distances):
                print(f"{doc} : {dist}")
                if (dist < 0.8 and distances[0] != 0.0):
                    output_dict[doc] = meta  # Assign the entire metadata dictionary
    

        return output_dict

    
    def see_collection(self):
        print(self.collection.get())





# vdb=VectorStore()
# # # # questions=["most booked hotel","most booked hotel in Mexico","most booked airline","trend of hotel booking season wise"]
# # # # for question in questions:
# # # #     vdb.add_question(question,'sql_test')

# vdb.see_collection()
# # while True:
# #     query=input("Query : ")
# #     print('Result **************')
# #     print(vdb.query_vdb(query,1))
