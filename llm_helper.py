from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr
import os


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=SecretStr(api_key) if api_key is not None else None, model='openai/gpt-oss-120b')


if __name__ == "__main__":
    response = llm.invoke("What are the Ingredients to make Chicken Biryani?")
    print(response.content)
