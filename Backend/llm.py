from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from Backend.config import MISTRAL_API_KEY
from Backend.config import GOOGLE_API_KEY
llm2 = ChatMistralAI(
    model="mistral-large-latest",
    api_key=MISTRAL_API_KEY,
    temperature=0.3
)
llm = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    api_key = GOOGLE_API_KEY,
    temperature = 0.3
)