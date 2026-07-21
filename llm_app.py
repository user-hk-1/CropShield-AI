import os
from dotenv import load_dotenv

# Load the hidden variables from your .env file
load_dotenv()

def llm_app(pesticide_name, crop_name):
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq
    
    # 1. Initialize your LLM securely using the environment variable
    groq_api = os.getenv("GROQ_API_KEY")
    
    # Upgraded to Llama3 for faster processing
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=groq_api, temperature=0.2)

    # 2. The Agritech Prompt
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

    # 3. Chain and Invoke
    chain = prompt | llm
    
    # Passing BOTH variables into the prompt perfectly
    output = chain.invoke({'pesticide': pesticide_name, 'crop': crop_name})
    
    return output.content