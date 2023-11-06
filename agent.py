import os
from langchain.agents import initialize_agent, Tool
from langchain.utilities import SerpAPIWrapper
from langchain.agents import AgentType
from langchain.llms import OpenAI
from gorilla import get_gorilla_response, raise_issue
from dotenv import load_dotenv
import openai

load_dotenv(".env")

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
search = SerpAPIWrapper()


def generate_response(question):
    llm = OpenAI(temperature=0)

    def gorilla_response(*args):
        try:
            return get_gorilla_response(question)
        except Exception as e:
            raise_issue(e, question)

    tools = [Tool(name = "Find information on Google", func = search.run, description = "This tool looks up top search results for a query. Pass in your query as a parameter. Do not write code."),
             Tool(name = "Generate code", func = gorilla_response, description = "The function generates code for how to address the given question. Pass the question in as a parameter. Return this code to the user. ")]
    agent = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True)

    result = agent.run({"input": question, "chat_history": []})

    return result

if __name__ == "__main__":
    result = generate_response("Google data on Apple's stock price history and use this data to generate code to predict future stock prices.")
    print(result)


