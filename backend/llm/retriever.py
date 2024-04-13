from wrappers.gemini_embedding import GeminiEmbeddingClient
from wrappers.gemini_chat import GeminiClient
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

class GeminiWrapper(GeminiEmbeddingClient):
    def __init__(self):
        super().__init__()

    def embed_documents(self, documents):
        return super().__call__(documents, batch=True)
    
def chunk_text(text: str) -> list[str]:
    text_splitters = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitters.split_text(text)

class Retriever:
    def __init__(self, docs: list[str], top_k: int = 4):
        db = FAISS.from_texts(docs, GeminiWrapper())
        faiss_retriever = db.as_retriever(search_kwargs={"k": top_k})
        bm25_retriever = BM25Retriever.from_texts(docs)
        ensemble_retriever = EnsembleRetriever(
            retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5]
        )
        self.retriever = ensemble_retriever

    def __call__(self, query: str):
        return self.retriever.invoke(query)
    
if __name__ == "__main__":
    with open("examples/sample_transcript.txt", "r") as f:
        transcript = f.read()

    r = Retriever(chunk_text(transcript))
    print(r("earnings call"))
    print(len(r("earnings call")))
