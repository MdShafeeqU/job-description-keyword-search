from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
import google.generativeai as genai
from flask_cors import CORS
import os
import nltk
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')
app = Flask(__name__)
CORS(app)

def generateJobTemplate(job_description):
    jobTemplate = f"""I have the following Job Description:
                {job_description}
                Based on the above job description, extract technical keywords that best describe the 
                skillsets and technologies required for the above job. Pay special attention to programming 
                languages, tools, and technologies mentioned.  Exclude any skills that are not present in the {job_description}. 
                List the education (only the degree, no majors) and experience if present in the job description too. 
                Ensure consistency in results across multiple tries.
                Use the following format:
                Skills: <keywords> 
                Experience: <number of years>
                Education: <Degree Type>"""
    return jobTemplate

def generateResumeTemplate(resume, skillsFromJob):
    resumeTemplate = f"""I have the following resume:
            {resume}
            Extract technical skills from the above resume. Extract skills that best describe the skillset and technologies that the resume-holder knows.
            These skills can include programming languages, tools, frameworks and technologies. Match the skills present in resume with the skills 
            extracted from the job description in the previous step.
            Here are the skills extracted from the job description:
            {skillsFromJob}"""
    return resumeTemplate

def generate_content(job_description, resume):
   GEMINI_API_KEY = os.environ.get('')
   genai.configure(api_key='AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM')
   llm = genai.GenerativeModel('gemini-pro')

   jobDescriptionPromptTemplate = PromptTemplate(input_variables=["job_description"], template=generateJobTemplate)
   #creating first chain
   keywordChain = LLMChain(llm=llm, prompt=jobDescriptionPromptTemplate, output_key="skillsFromJob")
   resume_prompt_template = PromptTemplate.from_template(generateResumeTemplate)
   resumeChain = LLMChain(llm=llm, prompt=resume_prompt_template, output_key="resumeOutput")
   input_data = {
    "job_description": job_description,
    "resume": resume
    }
   sequential_chain = SequentialChain(
        chains=[keywordChain, resumeChain],
        input_variables=["job_description","resume"],
        output_variables=["skillsFromJD","resumeOutput"],
        verbose=True
    )
   output_data = sequential_chain(input_data)
   return ""

def find_matching_keywords(extracted_keywords, resume_text):
     # Define a regular expression to match only alphabetic characters
    alpha_regex = re.compile('[^a-zA-Z]+')
    exclude_words = {'education', 'skills', 'experience', "master's", "bachelor's"}

    # Tokenize, filter out non-alphabetic characters, exclude specific words and numbers
    keywords = set(filter(lambda word: alpha_regex.sub('', word) and word.lower() not in exclude_words and not word.isdigit(),
                        word_tokenize(extracted_keywords.lower())))
    
    resume_words = set(filter(lambda word: alpha_regex.sub('', word) and word.lower() not in exclude_words and not word.isdigit(),
                        word_tokenize(resume_text.lower())))
    
    # Tokenize and filter out non-alphabetic characters
    # keywords  = set(filter(lambda word: alpha_regex.sub('', word), word_tokenize(extracted_keywords.lower())))
    # resume_words  = set(filter(lambda word: alpha_regex.sub('', word), word_tokenize(resume_text.lower())))
    print("Resume_words", resume_words)
    
    matching_keywords = keywords.intersection(resume_words)
    print("Matching keywords: ", matching_keywords)
    percentage = (len(keywords.intersection(resume_words)) / len(keywords)) * 100 if len(keywords) > 0 else 0
    print(percentage)
    string = ', '.join(list(matching_keywords))
    string = string + "Percentage: "+ str(round(percentage))
    return string

@app.route('/match', methods = ['GET', 'POST'])
def match_resume():

    data = request.get_json()

    resume_text = data.get('resumeText','')
    extracted_keywords = data.get('extractedKeywords','')

    res = find_matching_keywords(extracted_keywords, resume_text)
    print(res)

    return jsonify({'Result': res })

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    processed_text = generate_content(selected_text)

    print(processed_text)
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
