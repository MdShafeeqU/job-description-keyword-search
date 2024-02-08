from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
CORS(app)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_content(job_description):
   try:
    GEMINI_API_KEY = os.environ.get('')
    if not GEMINI_API_KEY:
       raise ValueError("GEMINI_API_KEY environment variable is not set")
    genai.configure(api_key=' ')
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(f"""I have the following Job Description:
                    {job_description}
                    Based on the above job description, extract technical keywords that best describe the 
                    skillsets and technologies required for the above job. Pay special attention to programming 
                    languages, tools, and technologies mentioned.  Exclude any skills that are not present in the {job_description}. 
                    List the education (only the degree, no majors) and experience if present in the job description too. 
                    Ensure consistency in results across multiple tries.
                    Use the following format:
                    Skills: <keywords> 
                    Experience: <number of years>
                    Education: <Degree Type>
                    """)
    return response.text
   except Exception as e:
    logger.error(f"An error occurred in generate_content: {str(e)}")
    return f"Error: {str(e)}"

@app.route('/', methods = ['GET','POST'])
def process_request():
    try:
        data = request.get_json()

        selected_text = data.get('text','')
        processed_text = generate_content(selected_text)

        logger.info(f"Processed text: {processed_text}")
        return jsonify({'processed_text': processed_text})
    except Exception as e:
       logger.error(f"An error occurred in process_request: {str(e)}")
       return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
