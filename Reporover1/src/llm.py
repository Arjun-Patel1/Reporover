# src/llm.py
from langchain_ollama import ChatOllama

def get_llm(model_name="llama3.1", temperature=0.1):
    """
    Initializes a local Ollama model.
    Benefits: Free, private, unlimited usage.
    """
    print(f"🔌 Connecting to local Ollama model: {model_name}...")
    
    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
        # Increase context window if your machine allows (e.g., 4096 or 8192)
        num_ctx=4096, 
    )
    return llm

if __name__ == "__main__":
    # Test connection
    try:
        llm = get_llm()
        print("Testing local brain...")
        response = llm.invoke("Write a 'Hello World' function in Python.")
        print(f"\nResponse:\n{response.content}")
    except Exception as e:
        print(f"❌ Error: Make sure Ollama is running! ({e})")