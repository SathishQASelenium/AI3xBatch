import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

def main():
    llm = ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "gemma3:4b"),
        temperature=1,
    )
    query = input("Enter the question: ")
    response = llm.invoke(query)
    print(response.content)

if __name__ == "__main__":
    main()