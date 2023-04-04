

from flask import Flask, render_template, request, Response
from flask_restful import Api, Resource

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, LLMSingleActionAgent, AgentOutputParser, ZeroShotAgent, Tool, AgentExecutor
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.callbacks.base import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import os
import openai
import pinecone 

  
app =   Flask(__name__)
  
api =   Api(app)

# Este en nuestro code que no podemos streamear

# MODEL = "text-embedding-ada-002"
# embeddings = OpenAIEmbeddings(openai_api_key="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")

# # initialize pinecone
# pinecone.init(
#     api_key="c679fb7d-cd38-4405-85b5-3ba2e223d833",  # find at app.pinecone.io
#     environment="us-west4-gcp"  # next to api key in console
# )

# index_name = "sample-test"
# index = pinecone.Index(index_name)

# def vb_retrieve(query: str) -> str:
#   embedded_query = openai.Embedding.create(input=query, engine=MODEL)['data'][0]['embedding']
#   res = index.query(embedded_query, top_k=5, namespace='wikimusculos-v0', include_metadata=True)
#   return '\n'.join([f'score: {r["score"]}, product information: {r["metadata"]["text"]}' for r in res['matches']])

# customTool = Tool(
#     name="vb_retrieval",
#     func=vb_retrieve,
#     description="useful for when you need to answer questions about products"
# )

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# tools = [ customTool ]

# prefix = """You are an AI assistant providing helpful advice.
#   You are a seller, be nice, try to upsell and cross-sell, but don't be pushy.
#   Explain why you are recommending something.
#   Provide a conversational answer based on the products available.
#   Do NOT make up products and try not to recommend products that you can't find with the available tools.
#   You have access to the following tools to search for products:"""
# suffix = """Begin!"

# {chat_history}
# Question: {input}
# {agent_scratchpad}"""

# prompt = ZeroShotAgent.create_prompt(
#     tools, 
#     prefix=prefix, 
#     suffix=suffix, 
#     input_variables=["input", "chat_history", "agent_scratchpad"]
# )

# llm = ChatOpenAI(
#     temperature=0,
#     openai_api_key="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", 
#     model_name="gpt-3.5-turbo"
# )
# llm_chain = LLMChain(llm=llm, prompt=prompt)
# agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
# agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memory)



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Esto es lo del ejemplo
def gen_prompt(query) -> str:
    return f"""To answer the question please only use the Context given, nothing else. Do not make up answer, simply say 'I don't know' if you are not sure.
    Question: {query}
    Context: You are an AI assistant providing helpful advice.
    Answer:
    """

def prompt(query):
     prompt = gen_prompt(query)
     return prompt

def stream(input_text):
        # Esto es lo del ejemplo
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "You're an assistant."},
            {"role": "user", "content": f"{prompt(input_text)}"},
        ], stream=True, max_tokens=500, temperature=0)
        
        # completion = agent_chain.run("say something about the product IPHONE 12")
        for line in completion:
            if 'content' in line['choices'][0]['delta']:
                yield line['choices'][0]['delta']['content']

@app.route('/completion', methods=['GET', 'POST'])
def completion_api():
    if request.method == "POST":
        input_text = "say something about the product IPHONE 12"
        return Response(stream(input_text), mimetype='text/event-stream')
    else:
        return Response(None, mimetype='text/event-stream')
    
if __name__ == '__main__':
    app.run(debug=True)