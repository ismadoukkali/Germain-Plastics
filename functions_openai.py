# Import from standard library
import logging
import streamlit as st
import openai
import os
from llama_index import LLMPredictor, ServiceContext, SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI
from llama_index.output_parsers import LangchainOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from llama_index.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from llama_index.prompts.default_prompts import DEFAULT_TEXT_QA_PROMPT_TMPL, DEFAULT_REFINE_PROMPT_TMPL
from llama_index import StorageContext, load_index_from_storage

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI']
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.5, model_name="gpt-4"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
storage_context = StorageContext.from_defaults(persist_dir='./storage')
index = load_index_from_storage(storage_context)
QA_PROMPT_TMPL = (
    "We have provided context information below regarding Geosynthetics Industrial Products. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given this information, recommed a product for a user's specific project, here the user's project: '{query_str}'"
    "Make your recommendation follow this format: \n"
    "\nFor a [project name], we recommend you look at our [product name]. [Give a description of what the product is, in one line - make the description specific to the given project.]\n"   
    "\n[product name] can:\n"
    "\nBulleted list:"
    "- [Mention 3 benefits of this product for the specific project - it has to explain why this benefit is useful for this specific project]\n"   
    "\nSpecs:"
    "\nBulleted list:"
    "- [Product specs]"
    "[Make sure you include the '**']"
    "\n**Project: [project name]**"
    "\n**Product: [product name]**"

    "Always answer in the format given above and use the full name of the product, do the correct differentiation between the product selected and the rest."
    "Finally, if the answer is not contained in the context, answer the following: 'I am not able to give an anwer to this search query, check further information in our website https://geosyn.com.au/ - '.\n"
)
QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)
logging.getLogger("openai").setLevel(logging.WARNING) 
 
class OpenAi:
    @staticmethod
    def retrieve_prompt(prompt: str) -> bool:     
        # try:
        query_engine = index.as_query_engine( text_qa_template=QA_PROMPT)
        response = query_engine.query(prompt)
        # except Exception as e:
        return response
    
    @staticmethod
    def prompt_organized(prompt: str) -> bool:
        response_schemas = [ResponseSchema(name="Product", description="Product Selected"),
        ResponseSchema(name="Project", description="Project for which the product will be applied"),
        ResponseSchema(name="Product_Description", description= "Brief description of the product and why it works for the project"),
        ResponseSchema(name="Product benefits", description="Three bulletpoints of why this product is beneficial for the project"),
        ResponseSchema(name="Specs", description="Specifications of the product")]
        lc_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        output_parser = LangchainOutputParser(lc_output_parser)
        fmt_qa_tmpl = output_parser.format(DEFAULT_TEXT_QA_PROMPT_TMPL)
        fmt_refine_tmpl = output_parser.format(DEFAULT_REFINE_PROMPT_TMPL)
        qa_prompt = QuestionAnswerPrompt(fmt_qa_tmpl, output_parser=output_parser)
        refine_prompt = RefinePrompt(fmt_refine_tmpl, output_parser=output_parser)
        query_engine = index.as_query_engine()
        response = query_engine.query(
            prompt, 
            text_qa_template=qa_prompt,
            refine_template=refine_prompt)
        return response