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

resume = """MEGHNA BAJORIA
meghnabajoria8@gmail.com • +1(620) 391-3957 • San Jose, CA
• linkedin.com/in/meghna-bajoria/ • github.com/meghnabajoria
WORK EXPERIENCE
Open-Source SoftwareDeveloper San Jose, CA
Google Summer of Code (The MifosInitiative) May 2023 – August 2023
• Developed a chatbot utilizing Spring Boot and Rasa Natural Language Processing (NLP) framework. Involved in designing 
and coding conversational flows, and training the chatbot to understand loan account inquiries from users
• Enhanced intent recognition accuracy by 25%, leading to optimized dialogue management processes
Software Engineer Bangalore, IN
Quinbay Technologies – Blibli.com Feb 2021 – June 2022
• Revamp multiple microservices, developed a price segmentation model in SpringBoot that boosted the GMV of the
application by 12%
• Managed Elastic Search for the team and independently improved search query performance by 58% using pagination
• Designed and implemented a secure data pipeline on GCP, ensuring application-exclusive access with IAM roles, setting the 
foundation for consistent and reliable data sources vital for advanced analytics and modeling
• Extracted and pre-processed data from BigQuery for advanced analytics and model training
Software EngineerIntern Gandhinagar, IN
Capgemini May 2019 – June 2019
• Analysed system log files from Optia Apheresis System and used C++ to extract data required for proper maintenance, 
facilitating focus on patient healthcare. Moved cleaned data to an SQL database for further analysis
• Optimized data processing steps using appropriate data structures, resulting in an 80% reduction in code execution time
• Implemented a data retrieval tool, enabling efficient extraction of relevant information from the database for further 
statistical analysis
CERTIFICATIONS
• AWS Cloud Practitioner
EDUCATION
Master of Science in Artificial Intelligence Graduating in May 2024
San Jose State University, San Jose, CA
Coursework: Natural Language Processing, Machine Learning, Artificial Intelligence, Recommendation Systems, Data Structures
Bachelor of Technology in Information Technology June 2021
Vellore Institute of Technology, Vellore, India
Coursework:Operating Systems, Computer Architecture, Database technologies, Web development, Software Testing
SKILLS
• Languages And Databases: Python, JavaScript, R, SQL, Java, Postgres, MongoDB
• Generative AI: Generative AI, Large Language Models, Google-Gemini, GPT API, Prompt Engineering, Creative Content 
Generation, LangChain, Huggingface, Fine Tuning, Diffusion Models
• Frameworks and Cloud Services: TensorFlow, MLOps, Flask, Vue.js, Docker, Google Cloud, AWS, Microsoft Azure, Amazon
Kinesis, Apache Flink, DynamoDB, CI/CD, Spark
• Other: Numpy, Pandas, scikit-learn, Cuda, HPC, Apache Kafka, REST API, Git, Elastic Search, Jenkins, Kibana, Stash, Splunk, Jira
PROJECTS
Job Analyzer – a keyword detection tool
Link: https://github.com/meghnabajoria/job-description-keyword-search
• Developed a Chrome extension to detect technical skills in a job description. Used Large Language Model (Google-Gemini), 
in conjunction with prompt engineering
• Used JavaScript and Flask to develop the extension. Deployed on Google Cloud Run for scalability and accessibility
Smart Quiz Builder
Link: https://github.com/meghnabajoria/mcqgen
• Automated the generation of fill-in-the-blank questions from provided text inputs, integrated GPT API to achieve the same
• Implemented the application using Python, facilitating seamless interaction with the GPT API
Financial-Analyst Chatbot
Link: https://github.com/meghnabajoria/Financial-Analyst
• Developed a finance information chatbot using Flask and Python, sourcing data from the Kiplinger website and integrating 
web scraping for search results.
• Utilized the GPT API to process user queries and generate informative responses, enhancing the chatbot's conversational 
capabilities."""

jobDescription = """
Summary
We are looking for an expert machine learning and data science engineer who can provide the ML services to data scientists, create AI solutions, scale up the ML models, manage the ML Ops, and perform needed governance tasks around deployed models. This person will be the backbone of the AI ML CoE department and will work on new age GenAI solutions. This person should be open to learn and implement new relevant tools and use cases. This person should be able to create the complete solution, so full stack development skill with experience of visualization/UX/UI will help a lot. This person will work in SAFe agile framework, so should have knowledge around it. This person should be very good at communication and in a collaborative environment.
Responsibilities
Responsibilities of the role are listed below but not limited to
• Provide ML services to data scientists, such as data preparation, feature engineering, model selection, optimization, deployment, and monitoring.
• Work closely with product SMEs, data scientists, and other stakeholders to understand the business requirements, use cases, and objectives of AI and ML initiatives.
• Design, develop, and deploy end-to-end AI and ML solutions using AWS services, Dataiku, Python, and other relevant technologies.
• Enable new features and capabilities of products into our AI and ML ecosystems, ensuring scalability, reliability, security, and performance.
• Scale up the ML models to handle large volumes of data and requests, using Dataiku and AWS services such as S3, EC2, Lambda, SageMaker, etc.
• Provide technical guidance and support to data scientists and other AI and ML users, facilitating knowledge sharing and collaboration.
• Manage the ML Ops, such as version control, testing, continuous integration, continuous delivery, continuous monitoring, troubleshooting of deployed ML models and pipelines.
• Learn and implement new relevant tools and use cases, such as Dataiku features, AWS AI services, ML frameworks, libraries, APIs, Azure AI stack etc.
• Create the complete solution, from data ingestion to user interface, using full stack development skills and experience of visualization/UX/UI.
• Communicate and collaborate effectively with stakeholders, such as business users, data scientists, developers, testers, etc.
• Integrate various data sources and platforms with our AI and ML platform, using best practices and standards.
• Create and maintain documentation, reports, and presentations on AI and ML projects and solutions.
• Perform governance and compliance tasks related to AI and ML, such as data quality, ethics, privacy, and auditability.
• Research and implement new and emerging tools, techniques, and trends in AI and ML, especially in the domain of GenAI.
• Work in a SAFe agile framework, following the principles and practices of agile development.
Qualifications
• Bachelor's degree or higher in computer science, engineering, mathematics, statistics, or related field.
• At least 5 years of experience in machine learning and data science, with proven track record of delivering successful AI solutions.
• Expert level skill in Dataiku.
• Expert level skill in AWS services, such as S3, EC2, Lambda, SageMaker, etc.
• Proficient in Python, R, SQL, and other programming languages for data analysis and ML development.
• Familiar with ML frameworks, libraries, and APIs, such as TensorFlow, PyTorch, Keras, Scikit-learn, Pandas, NumPy, etc.
• Knowledgeable in ML concepts, techniques, and algorithms, such as supervised learning, unsupervised learning, deep learning, etc.
• Experienced in full stack development, with skills in web development, visualization, UX/UI, etc.
• Proficient in various ML best practices, standards, and methodologies, such as SAFe agile, ML Ops, ML governance, etc.
• Expert in Azure and other cloud platforms, and willingness to learn and adapt to new technologies.
• Excellent communication and collaboration skills, with ability to explain complex technical concepts to non-technical audiences.
• Strong problem-solving and analytical skills, with attention to detail and quality.
• Curious and passionate about learning new things and exploring new possibilities in AI and ML.
Requirement summary:
1. Behaviour requirement
• Fast learner
• Collaborative nature
• Share knowledge with everyone and always eager to teach or uplift other skills, if provided opportunities
• Structured person
• Solution oriented person
• Good documentation practices
• Confident to speak with data scientists and help them in solving day to day challenge on data science.
• Confident to speak with data engineers and help them in solving day to day challenge.
• Confident speaker to present solution in business language.
• Professional and respectful attitude.
• Be able to read the shared material (I.e. Blogs) and quick to create quick PoC.
• Proactive: - Be persistence to gain access or information and don’t just keep waiting for another team to respond


2. Process requirements
• Understand SAFe Agile setup!
• Experience in envisioning AI product, divide it into features and then guide small team to divide further into user stories.
• Technology and Solution Architecture experience
• Experience with visualisation and UI/UX will be preferred.


3. Technology Requirement
• Data Science and Machine Learning – Expert
• AWS eco-system – Expert
• Dataiku – Expert
• Deployment model – Expert
• Governance of Models after deployment – expert
• Operations and support matrix for production models – expert
• Experienced in GenAI and keep up with recent development – experienced in using LLMs/GenAI, creating solutions and hosting as well as training LLMs.
• Explorer to CI/CD - Expert
• Experienced in full stack - good exposure with some experience.
• Experienced in Azure AI technology stack – to use OpenAI
"""

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
            These skills can include programming languages, tools, frameworks and technologies. Match the skills present in resume with the skills 
            extracted from the job description in the previous step.
            Here are the skills extracted from the job description:
            {skillsFromJob}"""
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

def find_matching_keywords(extracted_keywords, resume_text):
     # Define a regular expression to match only alphabetic characters
    alpha_regex = re.compile('[^a-zA-Z]+')
    exclude_words = {'education', 'skills', 'experience', "master's", "bachelor's"}

    # Tokenize, filter out non-alphabetic characters, exclude specific words and numbers
    keywords = set(filter(lambda word: alpha_regex.sub('', word) and word.lower() not in exclude_words and not word.isdigit(),
                        word_tokenize(extracted_keywords.lower())))
    
    resume_words = set(filter(lambda word: alpha_regex.sub('', word) and word.lower() not in exclude_words and not word.isdigit(),
                        word_tokenize(resume_text.lower())))
    
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

    return jsonify({
                    "jd_keywords": res["skillsFromJob"], 
                    "resume_match": res["resumeOutput"]
                     })

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    processed_text = generate_content(jobDescription, resume)

    print(processed_text)
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
