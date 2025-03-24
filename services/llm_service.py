import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
xai_api_key = os.environ.get("XAI_API_KEY")

# Initialize clients
def get_client(provider="openai"):
    """Get the appropriate client based on the provider.
    
    Args:
        provider (str): The LLM provider to use ("openai", "xai")
        
    Returns:
        client: The appropriate client object
    """
    if provider == "openai":
        return OpenAI(api_key=openai_api_key)
    elif provider == "xai":
        return OpenAI(api_key=xai_api_key, base_url="https://api.x.ai/v1")
    else:
        st.error(f"Unsupported provider: {provider}")
        return None

def get_llm_response(prompt, system_message="You are a helpful assistant.", provider="openai", model=None):
    """Get response from LLM API.
    
    Args:
        prompt (str): The user prompt to send to the LLM
        system_message (str): The system message to set the context
        provider (str): The LLM provider to use ("openai", "xai")
        model (str, optional): The specific model to use. Defaults to provider's standard model.
        
    Returns:
        str: The LLM's response
    """
    try:
        client = get_client(provider)
        
        if not client:
            return "Failed to initialize client. Check API keys and dependencies."
        
        if model is None:
            if provider == "openai":
                model = "gpt-4o-mini"
            elif provider == "xai":
                model = "grok-1"
        
        # both openai and xai use the same api structure
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=600
        )
        return response.choices[0].message.content
            
    except Exception as e:
        st.error(f"Error communicating with {provider.upper()} API: {e}")
        return f"I'm having trouble processing your request with {provider}. Please try again later."