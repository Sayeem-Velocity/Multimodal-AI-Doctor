from dotenv import load_dotenv
load_dotenv()

import os
import base64
from groq import Groq


def encode_image(image_path: str) -> str:
    """
    Reads an image file from disk and encodes it into a base64 string.
    This is needed because the Groq multimodal API expects images
    as base64 data URIs.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        str: Base64-encoded image data
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_image_with_query(query: str, model: str, encoded_image: str) -> str:
    """
    Sends a text query + an encoded image to Groq's multimodal chat completion API.
    The LLM processes both modalities and returns a generated response.
    
    Args:
        query (str): The textual query/prompt (e.g., doctor's instruction)
        model (str): The Groq multimodal model to use (e.g., llama-4-scout)
        encoded_image (str): Base64-encoded image string
    
    Returns:
        str: The model's generated response
    """

    # Fetch Groq API key from environment variables
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in environment")

    # Initialize Groq client with API key
    client = Groq(api_key=api_key)

    # Construct the multimodal message payload:
    # - First element is plain text query
    # - Second element is image encoded as a base64 data URL
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}} 
            ],
        }
    ]

    # Call Groq's chat completion API with low temperature (0.1) for deterministic output.
    # Limit tokens to 1000 to control response length.
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0.1,
        max_tokens=1000
    )

    # Extract and return the model's response text
    return chat_completion.choices[0].message.content
