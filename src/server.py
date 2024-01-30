from flask import Flask, request, jsonify
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

app = Flask(__name__)

def generate_content(job_description):
   genai.configure(api_key="AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM")
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("""I have the following Job Description:
                {job_description}
                Based on the above job description, extract technical keywords that best describe the 
                skillsets and technologies required for the above job. Pay special attention to programming 
                languages, tools, and technologies mentioned.
                Use the following format separated by commas:
                <keywords>
                """)
   return response.text

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    # print('Text Selected: ', selected_text)

    processed_text = selected_text.upper()

    print("Processed Text: ", processed_text)
    processed_text = generate_content(processed_text)
    # return jsonify({'message': 'OK'})
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(port=8080)