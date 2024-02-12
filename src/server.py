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
                Education: <Degree Type>"""
    return jobTemplate

def generateResumeTemplate(resume, skillsFromJob):
    resumeTemplate = f"""I have the following resume:
            {resume}
            Extract technical skills from the above resume. Extract skills that best describe the skillset and technologies that the resume-holder knows.
            These skills can include programming languages, tools, frameworks and technologies. Exacly match the skills present in resume with the skills present in the given job description.
            Be very accurate in matching the keywords.

            Here are the skills extracted from the job description:
            {skillsFromJob}

            Give only the matching keywords. Use following format to return matching keywords seperated by commas:
            Matching Skills: <keywords> 
            """
        

    return resumeTemplate



def generate_content(jobDescription, resume):
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = "AIzaSyD2ut1rrUIzbOSFuW7g-0PT6MGIwjcFAXM"

    llm = ChatGoogleGenerativeAI(model="gemini-pro")

    # job description prompt template
    jobDescriptionPromptTemplate = PromptTemplate(input_variables=["jobDescription"], template=generateJobTemplate(jobDescription))

    # LLMChain for job description
    keywordChain = LLMChain(llm=llm, prompt=jobDescriptionPromptTemplate, output_key="skillsFromJob")

    # resume prompt template
    resumePromptTemplate = PromptTemplate.from_template(generateResumeTemplate(resume, "{skillsFromJob}"))

    # LLMChain for resume
    resumeChain = LLMChain(llm=llm, prompt=resumePromptTemplate, output_key="matchingSkills")

    inputData = {
        "jobDescription": jobDescription,
        "resume": resume
    }

    sequential_chain = SequentialChain(
        chains=[keywordChain, resumeChain],
        input_variables=["jobDescription", "resume"],
        output_variables=["skillsFromJob", "matchingSkills"],
        verbose=True
    )

    output_data = sequential_chain(inputData)
    print(output_data['skillsFromJob'])
    print(output_data['matchingSkills'])
    return output_data

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    resume_text = data.get('resumeText', '')

    # print(selected_text)
    # print(resume_text)

    res = generate_content(selected_text, resume_text)

    # print(processed_text)
    return jsonify({
                    "jd_keywords": res["skillsFromJob"], 
                    "resume_match": res["matchingSkills"]
                     })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
