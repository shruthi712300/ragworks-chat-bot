# import os
# import logging
# from typing import Optional
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load Gemini API key
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     logger.warning("⚠️ GEMINI_API_KEY not set. Responses will fall back to basic messages.")
#     genai_model = None
# else:
#     genai.configure(api_key=GEMINI_API_KEY)
#     try:
#         genai_model = genai.GenerativeModel("gemini-1.5-pro")
#         logger.info("✅ Gemini model loaded successfully")
#     except Exception as e:
#         logger.error(f"Error loading Gemini model: {e}")
#         genai_model = None


# def generate_response(prompt: str, context: Optional[str] = None) -> str:
#     """
#     Generate medical chatbot response using Google Gemini.
#     Includes optional RAG context.
#     """

#     if not genai_model:
#         return _fallback_response(prompt)

#     try:
#         system_prompt = (
#             "You are a knowledgeable medical assistant helping healthcare professionals and patients. "
#             "Provide accurate, evidence-based information in a clear, structured format. "
#             "Always remind users to consult a qualified healthcare professional."
#         )

#         if context:
#             user_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser question: {prompt}"
#         else:
#             user_prompt = f"{system_prompt}\n\nUser question: {prompt}"

#         response = genai_model.generate_content(user_prompt)

#         content = response.text.strip() if response and response.text else "⚠️ No response generated."
#         return f"{content}\n\n{medical_disclaimer()}"

#     except Exception as e:
#         logger.error(f"Error generating Gemini response: {e}")
#         return f"⚠️ I encountered an error while generating the response: {e}\n\n{medical_disclaimer()}"


# def _fallback_response(prompt: str) -> str:
#     """Fallback when Gemini API is unavailable"""
#     return (
#         f"⚠️ Gemini API key not configured. Unable to generate an intelligent response.\n\n"
#         f"You asked: {prompt}\n\n"
#         f"{medical_disclaimer()}"
#     )


# def train_custom_model(data_path: str) -> str:
#     """Placeholder for custom fine-tuning"""
#     logger.info(f"Custom model training requested for: {data_path}")
#     return "Custom training is not implemented. Consider using Vertex AI for fine-tuning with your medical dataset."


# def medical_disclaimer() -> str:
#     """Standard medical disclaimer"""
#     return (
#         "---\n"
#         "🏥 **Medical Disclaimer:** This information is for educational purposes only "
#         "and is *not* a substitute for professional medical advice, diagnosis, or treatment. "
#         "Always consult a qualified healthcare provider for clinical decisions."
#     )





import os
import logging
from typing import Optional
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD0g8tNOFgfJZJ2b8m5rECJWKEoWrIinCY")
genai_model = None

if not GEMINI_API_KEY:
    logger.warning("⚠️ GEMINI_API_KEY not set. Responses will fall back to basic messages.")
else:
    try:
        logger.info(f"API Key found: {GEMINI_API_KEY[:10]}...")  # Log first 10 chars
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Use the specific model that works: models/gemini-1.5-pro-latest
        genai_model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        logger.info("✅ Using model: models/gemini-1.5-pro-latest")
        
        # Test the model connection
        test_response = genai_model.generate_content("Hello")
        if test_response and test_response.text:
            logger.info("✅ Gemini model configured successfully and responding")
        else:
            logger.warning("⚠️ Model configured but test response failed")
        
    except Exception as e:
        logger.error(f"Error configuring Gemini: {e}")
        genai_model = None


def generate_response(prompt: str, context: Optional[str] = None) -> str:
    """
    Generate medical chatbot response using Google Gemini.
    Includes optional RAG context with proper safety handling.
    """
    if not genai_model:
        return _fallback_response(prompt)

    try:
        system_instruction = (
            "You are a knowledgeable medical assistant helping healthcare professionals and patients. "
            "Provide accurate, evidence-based information in a clear, structured format. "
            "Always remind users to consult a qualified healthcare professional. "
            "Be cautious and conservative in your recommendations. "
            "If you are unsure about something, say so rather than guessing."
        )

        # Build the prompt
        if context:
            full_prompt = f"{system_instruction}\n\nContext:\n{context}\n\nQuestion: {prompt}"
        else:
            full_prompt = f"{system_instruction}\n\nQuestion: {prompt}"

        # Generate response
        response = genai_model.generate_content(full_prompt)

        if not response or not response.text:
            return "⚠️ No response generated. Please try again.\n\n" + medical_disclaimer()

        return f"{response.text.strip()}\n\n{medical_disclaimer()}"

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"⚠️ Error: {str(e)[:100]}...\n\n{medical_disclaimer()}"


def _fallback_response(prompt: str) -> str:
    """Fallback when Gemini API is unavailable"""
    logger.warning("Using fallback response - Gemini API not available")
    return (
        f"⚠️ Gemini API key not configured. Unable to generate an intelligent response.\n\n"
        f"You asked: {prompt}\n\n"
        f"{medical_disclaimer()}"
    )


def train_custom_model(data_path: str) -> str:
    """Placeholder for custom fine-tuning"""
    logger.info(f"Custom model training requested for: {data_path}")
    return "Custom training is not implemented. Consider using Vertex AI for fine-tuning with your medical dataset."


def medical_disclaimer() -> str:
    """Standard medical disclaimer"""
    return (
        "---\n"
        "🏥 **Medical Disclaimer:** This information is for educational purposes only "
        "and is *not* a substitute for professional medical advice, diagnosis, or treatment. "
        "Always consult a qualified healthcare provider for clinical decisions. "
        "Do not delay seeking medical advice based on information provided here."
    )


# Optional: Add model health check function
def check_model_health() -> bool:
    """Check if the Gemini model is properly configured and accessible"""
    if not genai_model:
        return False
    
    try:
        # Simple test prompt to verify model connectivity
        test_response = genai_model.generate_content("Hello, are you working?")
        return test_response and test_response.text is not None
    except Exception as e:
        logger.error(f"Model health check failed: {e}")
        return False


if __name__ == "__main__":
    # Simple test if run directly
    print("Testing Gemini connection...")
    if check_model_health():
        print("✅ Model is healthy")
        test_response = generate_response("What are common symptoms of a cold?")
        print("Test response:", test_response[:200] + "...")
    else:
        print("❌ Model not available")