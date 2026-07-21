import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Load environment variables securely from .env
load_dotenv()

def llm_app(pesticide_name, crop_name):
    """Generates the main 4-point agricultural advisory report."""
    groq_api = os.getenv("GROQ_API_KEY")
    if not groq_api:
        raise ValueError("GROQ_API_KEY missing! Check your .env file.")

    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=groq_api, temperature=0.2)

    prompt = PromptTemplate(
        input_variables=['pesticide', 'crop'],
        template="""You are a Senior Agricultural Scientist and Certified Agronomist operating in India. Your primary objective is to provide highly accurate, science-based pesticide diagnostics and crop advisory to local farmers.

        You communicate with absolute clinical precision, authoritative knowledge, and a deeply professional tone. You must strictly avoid conversational filler.

        The user has scanned the chemical '{pesticide}' for use on '{crop}'.
        Generate a technical but accessible 4-point advisory report detailing:

        1. Target Pests: The precise biological targets of this chemical.
        2. Agronomic Benefits: Yield and protection advantages for '{crop}'.
        3. Ecotoxicity & Risks: Specific dangers to soil health, groundwater, and human handling.
        4. Sustainable Alternatives: Safer application methods or organic pest management strategies.
        5. Give only three pointers for each of the inputs."""
    )

    chain = prompt | llm
    output = chain.invoke({'pesticide': pesticide_name, 'crop': crop_name})
    return output.content

def llm_qa(pesticide_name, crop_name, user_question):
    """Answers follow-up questions from the farmer using Groq LLM."""
    groq_api = os.getenv("GROQ_API_KEY")
    if not groq_api:
        raise ValueError("GROQ_API_KEY missing! Check your .env file.")

    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=groq_api, temperature=0.3)

    prompt = PromptTemplate(
        input_variables=['pesticide', 'crop', 'question'],
        template="""You are an expert Agricultural Assistant and Senior Agronomist in India.
        
        CONTEXT:
        - Target Crop: {crop}
        - Detected Chemical: {pesticide}

        FARMER QUESTION: '{question}'

        INSTRUCTIONS:
        - Provide a direct, practical, and highly accurate answer suitable for a farmer.
        - Keep the response under 150 words.
        - Do not use conversational filler or meta-commentary."""
    )

    chain = prompt | llm
    output = chain.invoke({'pesticide': pesticide_name, 'crop': crop_name, 'question': user_question})
    return output.content