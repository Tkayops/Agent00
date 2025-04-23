import json
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_mistralai.chat_models import ChatMistralAI

# Define the LLM
llm = ChatMistralAI(model="mistral-tiny", temperature=0)

# Create the ranking prompt with escaped JSON template
ranking_prompt = PromptTemplate.from_template("""
You are a recruitment agent.

Given:
Job Description: {job}
Candidate Profile: {profile}

Return a JSON like:
{{
  "score": int (0-10),
  "reason": "why the candidate fits this job"
}}
""")

# Create the runnable chain using the new syntax
ranking_chain = ranking_prompt | llm

# Optional helper to safely extract JSON from string
def extract_json_from_response(text):
    try:
        # Attempt to parse the first valid JSON object
        start = text.find('{')
        end = text.rfind('}') + 1
        return json.loads(text[start:end])
    except Exception as e:
        return {
            "score": 0,
            "reason": f"Invalid JSON format: {str(e)}"
        }

# Main ranking function
def rank_candidate(job_text: str, profile_text: str):
    try:
        response = ranking_chain.invoke({"job": job_text, "profile": profile_text})
        # Handle different response formats
        raw_text = response.content if hasattr(response, 'content') else str(response)
        print("🔍 LLM Raw Response:\n", raw_text)
        result = extract_json_from_response(raw_text)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({
            "score": 0,
            "reason": f"Failed to rank due to error: {str(e)}"
        })
