import os
import sys
import constants
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

os.environ["OPENAI_API_KEY"] = constants.APIKEY

template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate.from_template(template)
llm = OpenAI()

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"
llm_chain = prompt | llm
print(llm_chain.invoke(question))