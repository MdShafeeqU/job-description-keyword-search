from flask import Flask, request, jsonify
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

import google.generativeai as genai
from flask_cors import CORS
import os
import nltk
import re

nltk.download('punkt')
app = Flask(__name__)
CORS(app)

def generateJobTemplate(jobDescription):
    jobTemplate = f"""I have the following Job Description:
                {jobDescription}
                Based on the above job description, we need to extract technical keywords, education (only the degree, no majors) and experience. The technical keywords should
                best describe the programming languages, tools, frameworks, and technologies present in the job description. Do not list any skill or technologies that is not present 
                in the job description.
                Ensure consistency in results across multiple tries.
                Use the following format strictly:
                Skills: <keywords> 
                Experience: <number of years>
                Education: <Degree Type>
                Return the skills, experience and education obtained from the job description and nothing else"""
    return jobTemplate

def generateResumeTemplate(resume):
    resumeTemplate = """
                    Find and match the technical skills obtained from the resume with the skills obtained from the job description.
                    Keep these points in mind.
                    Extract all the technical skills like programming languages, tools, technologies, frameworks and keywords from the resume. Then match all the skills that 
                    match between the resume and keywords in the job description. The matched skills should be complete and should not be repeated. Any skill which is not present 
                    in the job description should not be considered while matching. Please maintain consistency across multiple tries. The matched skills should be comma seperated in this format:
                    Matched Skills: <matched skills>
                    Resume:
                    {resume}

                    Skills from job description:
                    {skillsFromJob}
            """
    return resumeTemplate

def generate_content(jobDescription, resume):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM"

    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.5)

    # job description prompt template
    jobDescriptionPromptTemplate = PromptTemplate(input_variables=["jobDescription"], template=generateJobTemplate(jobDescription))

    # LLMChain for job description
    keywordChain = LLMChain(llm=llm, prompt=jobDescriptionPromptTemplate, output_key="skillsFromJob", verbose=True)
    
    # resume prompt template
    resumePromptTemplate = PromptTemplate(input_variables=["resume", "skillsFromJob"], template = generateResumeTemplate(resume))

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
