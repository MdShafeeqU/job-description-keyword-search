## Overview
This powerful tool is designed to streamline the job search experience by seamlessly finding technical keywords in a job description and matching those keywords with skills present in your resume. Powered by Python, Flask, and Google Gemini, this extension offers an intuitive interface and efficient keyword comparison capabilities.

## Features
- **Intelligent Keyword Matching:** Instantly compare keywords in your resume with those extracted from the job description, ensuring alignment with the employer's requirements. 
- **Seamless Integration:** With a user-friendly interface, simply upload your resume and the job description to initiate the matching process effortlessly.
- **Powered by Google Gemini:** Harness the advanced capabilities of Google Gemini for efficient and accurate keyword extraction and comparison.

## Contributing and Installation:
1. Virtual environment (use gitbash recommended)
- "conda create -p env python=3.9"
- "source activate ./env" or "conda activate ./env"
2. pip install flask
3. python src/server.py
4. Load the extension in Chrome
- "chrome://extensions/" -> Enable Developer Mode -> "Load Unpacked" -> Select the folder
5. To trigger extension: 
- Select text from any webpage -> right click -> Select SkillSearch

## Visual Walkthrough

![1](https://github.com/MdShafeeqU/job-description-keyword-search/assets/50470784/805e0155-6159-4501-b3e3-48f18384d8b2)
![2222](https://github.com/MdShafeeqU/job-description-keyword-search/assets/50470784/04089b99-8ec6-46d3-8d70-faefa373183b)
![3](https://github.com/MdShafeeqU/job-description-keyword-search/assets/50470784/0cc8c8d2-b065-4444-a830-19e88df31c08)
![44444](https://github.com/MdShafeeqU/job-description-keyword-search/assets/50470784/0909e3c2-7bfe-403d-950c-a26a4aaff230)

## Possible Improvement
- The LLM often gives inconsistent results, as evident from the screenshots.
-  Sequential processing entails executing tasks one after the other, leading to a cumulative delay in completing operations. 



