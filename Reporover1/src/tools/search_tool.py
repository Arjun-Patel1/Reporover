import os
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

class CodeSearchTool:
    def __init__(self, repo_path: str, persist_dir="./chroma_db"):
        self.repo_path = repo_path
        self.persist_dir = persist_dir
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = None

    def ingest_codebase(self):
        """
        Loads all Python files from the repo, chunks them, and stores them in ChromaDB.
        """
        print(f"Scanning codebase at {self.repo_path}...")
        
        # 1. Load the code
        loader = GenericLoader.from_filesystem(
            self.repo_path,
            glob="**/*",
            suffixes=[".py"],
            parser=LanguageParser(language=Language.PYTHON, parser_threshold=500),
        )
        documents = loader.load()
        
        # 2. Split the code into chunks (context-aware)
        python_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON, 
            chunk_size=2000, 
            chunk_overlap=200
        )
        texts = python_splitter.split_documents(documents)
        
        print(f"Created {len(texts)} chunks from codebase.")

        # 3. Create/Update the Vector Store
        self.db = Chroma.from_documents(
            documents=texts, 
            embedding=self.embeddings, 
            persist_directory=self.persist_dir
        )
        print("Ingestion complete. Vector DB ready.")

    def search(self, query: str, k=5):
        """
        Retrieves the top k most relevant code chunks for a query.
        """
        if not self.db:
            # Load existing DB if available
            self.db = Chroma(
                persist_directory=self.persist_dir, 
                embedding_function=self.embeddings
            )
            
        results = self.db.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

if __name__ == "__main__":
    # Test on the current directory
    tool = CodeSearchTool(repo_path="./src")
    tool.ingest_codebase()
    
    results = tool.search("How do we ingest code?")
    print("\n--- Search Results ---\n")
    for i, res in enumerate(results):
        print(f"Result {i+1}:\n{res[:200]}...\n")
        