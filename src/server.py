from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def generate_content(job_description):
   GEMINI_API_KEY = os.environ.get('')
   genai.configure(api_key='AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM')
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


@app.route('/match', methods = ['GET', 'POST'])
def match_resume():

    data = request.get_json()

    resume_text = data.get('resumeText','')
    extracted_keywords = data.get('extractedKeywords','')

    # print(resume_text)
    # print(extracted_keywords)
    # match_result = do_process(resume_text)
    return jsonify({'Status': 'Thanks for matching! Matched Keywords will be displayed here. Kindly be patient for this functoinality.'})

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    processed_text = generate_content(selected_text)

    print(processed_text)
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
