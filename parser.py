from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
import os
import json  # Add json module for parsing

load_dotenv()

llm = ChatMistralAI(model="mistral-tiny", temperature=0)

prompt = PromptTemplate.from_template(""" 
Extract the following from the job description:
- Job title
- Skills
- Years of experience
- Domain/industry
- Certifications

Return JSON with keys: job_title, skills, experience_years, domain, certifications

Job description:
{job_description}
""")

parser_chain = LLMChain(llm=llm, prompt=prompt)

def parse_job_description(text: str):
    result = parser_chain.run({"job_description": text})
    try:
        # Parse the string result into a JSON object (dictionary)
        parsed_result = json.loads(result)
        return parsed_result
    except json.JSONDecodeError:
        print("Failed to decode the result as JSON:", result)
        return None
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

response_schemas = [
    ResponseSchema(name="job_title", type="str", description="Job title"),
    ResponseSchema(name="skills", type="List[str]", description="List of required technical skills"),
    ResponseSchema(name="experience_years", type="str", description="Years of experience required"),
    ResponseSchema(name="domain", type="str", description="Industry domain"),
    ResponseSchema(name="certifications", type="List[str]", description="Required certifications")
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
prompt = PromptTemplate(
    template="Extract job details from this description:\n{job_description}\n{format_instructions}",
    input_variables=["job_description"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)