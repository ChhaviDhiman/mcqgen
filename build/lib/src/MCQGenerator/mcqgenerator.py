import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv
from MCQGenerator.utils import read_file,get_table_data
from MCQGenerator.logger import logging

import g4f
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

load_dotenv()

from langchain.llms.base import LLM
import g4f
from typing import Optional, List


class G4FLLM(LLM):
    model_name: str = "gpt_3_5_turbo"  # Define your model here, default is gpt_3_5_turbo from g4f

    # This method is responsible for making the API call to g4f's model
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            # Use g4f to generate the completion based on the prompt
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_3_5_turbo,
                messages=[{"role": "user", "content": prompt}]
            )
            # Extract the generated content from the response
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"

    # Required method for langchain to get identifying parameters for the model
    @property
    def _identifying_params(self) -> dict:
        return {"model_name": self.model_name}

    # Correct method to identify the type of LLM
    def _llm_type(self) -> str:
        return "g4f"

llm=G4FLLM()
template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=template)

quiz_chain=LLMChain(llm=llm,prompts=quiz_generation_prompt,output_key="quiz",verbose=True)

template2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""


quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=template2)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)


# This is an Overall Chain where we run the two chains in Sequence
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)