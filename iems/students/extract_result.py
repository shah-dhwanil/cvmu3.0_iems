import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from iems.base.config import Config

genai.configure(api_key=Config.get_config().GOOGLE_API_KEY)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    enum = [],
    required = ["student_name","program_name", "score", "year_of_apperance"],
    properties = {
      "student_name": content.Schema(
        type = content.Type.STRING,
      ),
      "program_name": content.Schema(
        type = content.Type.STRING,
      ),
      "score": content.Schema(
        type = content.Type.NUMBER,
      ),
      "year_of_apperance": content.Schema(
        type = content.Type.INTEGER,
      ),
    },
  ),
  "response_mime_type": "application/json",
}
SYSTEM_INSTRUCTION = """
You are a specialized document analysis assistant focused on extracting key information from educational marksheets and certificates. Your primary task is to analyze the provided marksheet and extract specific data points accurately.

Primary Data Points to Extract:
1. Student's Full Name
   - Look for fields labeled as "Name", "Student Name", "Candidate Name"
   - Extract the complete name including first name, middle name (if any), and last name
   - Maintain the exact case and spelling as shown in the document

2. Seat/Registration Number
   - Search for fields like "Seat No.", "Registration No.", "Roll No.", "Enrollment No."
   - Extract the complete number including any prefixes or suffixes
   - Preserve any special characters or formatting in the number

3. Educational Program Details
   - For Higher Secondary Education:
     * Look for "Examination Name" or "Course"
     * Usually appears as "HSC", "12th Standard", "Senior Secondary", etc.
     * Include the stream if mentioned (Science/Commerce/Arts)
   
   - For Higher Education:
     * Extract the complete degree name (e.g., "Bachelor of Engineering", "Master of Science")
     * Include specialization/major if mentioned
     * Note the type: Diploma/Undergraduate/Graduate/Postgraduate

4. Academic Performance Calculation
      Score in terms if percentage or CGPA/CPI.
      If individual scores are listed calculate the percentage by summing the marks of each subject and then dividing with (no of subjects*100)
5. Document Context:
   - Note the academic year or examination period if available
   - Include the name of issuing institution if present
   - Mention any special achievements or distinctions

Generate the response in JSON  it should only contain name of student, the exam score and program details and year of apperance
"""

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction=SYSTEM_INSTRUCTION
)

def extract_result(file_path: str,mime_type:str) -> dict:
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
    response = chat_session.send_message("Extract the data from the Marksheet")
    print(response.text)
    return response.text