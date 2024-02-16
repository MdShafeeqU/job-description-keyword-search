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

def generateJobTemplate(jobDescription):
    jobTemplate = f"""I have the following Job Description:
                {jobDescription}
                Based on the above job description, extract technical keywords that best describe the 
                skillsets and technologies required for the above job. Pay special attention to programming 
                languages, tools, and technologies mentioned.  Exclude any skills that are not present in the {jobDescription}. 
                List the education (only the degree, no majors) and experience if present in the job description too. 
                Ensure consistency in results across multiple tries.
                Use the following format:
                Skills: <keywords> 
                Experience: <number of years>
                Education: <Degree Type>
                Return the skills obtained from the job description and nothing else"""
    return jobTemplate


def generate_content(jobDescription, resume):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM"

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)

    # job description prompt template
    jobDescriptionPromptTemplate = PromptTemplate(input_variables=["jobDescription"], template=generateJobTemplate(jobDescription))

    # LLMChain for job description
    keywordChain = LLMChain(llm=llm, prompt=jobDescriptionPromptTemplate, output_key="skillsFromJob", verbose=True)
    
    resumeTemplate = """
                    Task: Find and match the technical skills obtained from the given resume with the skills obtained from the job description.
                    Keep these points in mind.
                    1. Extract all the technical skills from the resume that best describe the skillsets, programming languages, tools and technologies 
                    that the resume holder knows.
                    2. Match all the skills that match between the resume and keywords in the job description.
                    2. The matched skills should be complete.
                    3. The matched skills should not be repeated.
                    4. Any skill which is not present in the job description should not be considered while matching.
                    5. If resume is empty then return nothing.
                    5. Maintain consistency across multiple tries
                    6. The matched skills should be comma seperated with the following format.
                        Matched Skills: <matched skills>
                    Resume:
                    {resume}

                    Skills from job description:
                    {skillsFromJob}
            """
    
    # resume prompt template
    resumePromptTemplate = PromptTemplate(input_variables=["resume", "skillsFromJob"], template = resumeTemplate)

    # LLMChain for resume
    resumeChain = LLMChain(llm=llm, prompt=resumePromptTemplate, output_key="matchingSkills", verbose=True)

    sequential_chain = SequentialChain(
        chains=[keywordChain, resumeChain],
        input_variables=["jobDescription","resume"],
        output_variables=["skillsFromJob", "matchingSkills"],
        verbose=True
    )

    print("Skills from job passed to the second chain:", sequential_chain.input_variables)


    output_data = sequential_chain.invoke(input={"jobDescription": jobDescription,"resume": resume})
    print(output_data['skillsFromJob'])
    print(output_data['matchingSkills'])
    return output_data

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    resume_text = data.get('resumeText', '')

    res = generate_content(selected_text, resume_text)

    return jsonify({
                    "jd_keywords": res["skillsFromJob"], 
                    "resume_match": res["matchingSkills"]
                     })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
