import os
from dotenv import load_dotenv
import openai
import urllib.parse

load_dotenv(".env")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

# Alternate mirrors
# openai.api_base = "http://34.132.127.197:8000/v1"

# Report issues
def raise_issue(e, prompt):
    issue_title = urllib.parse.quote("[bug] Hosted Gorilla: <Issue>")
    issue_body = urllib.parse.quote(f"Exception: {e}\nFailed model: gorilla-7b-hf-v1, for prompt: {prompt}")
    issue_url = f"https://github.com/ShishirPatil/gorilla/issues/new?assignees=&labels=hosted-gorilla&projects=&template=hosted-gorilla-.md&title={issue_title}&body={issue_body}"
    print(f"An exception has occurred: {e} \nPlease raise an issue here: {issue_url}")

# Query Gorilla server
# api_base = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
def get_gorilla_response(prompt):
  try:
    openai.api_base = "http://zanino.millennium.berkeley.edu:8000/v1"
    completion = openai.ChatCompletion.create(
      model="gorilla-7b-hf-v1",
      messages=[{"role": "user", "content": prompt}]
    )
    openai.api_base = "https://api.openai.com/v1" 
    return completion.choices[0].message.content
  except Exception as e:
    raise_issue(e, prompt)