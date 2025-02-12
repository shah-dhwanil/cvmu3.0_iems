import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from iems.base.config import Config

genai.configure(api_key=Config.get_config().GOOGLE_API_KEY)
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 512,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    enum = [],
    required = ["first_name", "last_name", "father_name", "dob", "address", "mobile_no", "aadhaar_no"],
    properties = {
      "first_name": content.Schema(
        type = content.Type.STRING,
      ),
      "last_name": content.Schema(
        type = content.Type.STRING,
      ),
      "father_name": content.Schema(
        type = content.Type.STRING,
      ),
      "dob": content.Schema(
        type = content.Type.STRING,
      ),
      "address": content.Schema(
        type = content.Type.STRING,
      ),
      "mobile_no": content.Schema(
        type = content.Type.STRING,
      ),
      "aadhaar_no": content.Schema(
        type = content.Type.STRING,
      ),
    },
  ),
  "response_mime_type": "application/json",
}

SYSTEM_INSTRUCTION = """
You are an AI assistant specialized in extracting information from Aadhaar cards, India's unique identification document. Your task is to accurately extract and structure specific personal information from Aadhaar card images while maintaining strict data privacy and security standards.

TASK REQUIREMENTS:
1. Extract the following fields from the provided Aadhaar card:
   - First Name(first_name)
   - Last Name(last_name)
   - Father's Name(father's_name)
   - Date of Birth (in DD/MM/YYYY format)
   - Complete Address(address)
   - Mobile Number (10 digits)(m_no)
   - Aadhaar Number (12 digits)(aadhaar_no)

OUTPUT FORMAT:
Return the extracted data in the following JSON structure
"""

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction=SYSTEM_INSTRUCTION
)

def extract_aadhaar(file_path: str,mime_type:str) -> dict:
    print(file_path,mime_type)
    file = genai.upload_file(file_path, mime_type=mime_type)
    chat_session = model.start_chat(
    history=[
        {
        "role": "user",
        "parts": [
            file,
        ],
        },
    ]
    )
    response = chat_session.send_message("Extract the data from the Aadhaar card")
    print(response.text)
    return response.text