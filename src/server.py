from flask import Flask, request, jsonify
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

app = Flask(__name__)

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def generate_content(job_description):
   genai.configure(api_key="insert your api key")
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("""I have the following Job Description:
                {document}
                Based on the above job description, extract technical keywords that best describe the 
                skillsets and technologies required for the above job. Pay special attention to programming 
                languages, tools, and technologies mentioned.
                Use the following format separated by commas:
                <keywords>
                """)
   to_markdown(response.text)

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    # print('Text Selected: ', selected_text)

    processed_text = selected_text.upper()

    print("Processed Text: ", processed_text)
    markdown_output = to_markdown(generate_content(processed_text))
    # return jsonify({'message': 'OK'})
    return jsonify({'keywords': markdown_output})

if __name__ == '__main__':
    app.run(port=8080)