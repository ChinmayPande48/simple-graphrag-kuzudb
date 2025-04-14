from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_kuzu.graphs.kuzu_graph import KuzuGraph
from langchain_kuzu.chains.graph_qa.kuzu import KuzuQAChain
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
import os
from os.path import join, dirname
from dotenv import load_dotenv
from graph_db import db

load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

graph = KuzuGraph(db, allow_dangerous_requests=True)
schema=graph.get_schema

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=GOOGLE_API_KEY,
    verbose=True,
    model_kwargs={"max_new_tokens":7000,"temperature": 0.1, "top_k": 1, "top_p": 0.95}
)

cypher_prompt_template_kuzuQAChain = PromptTemplate(input_variables=[schema,"question"],
    template="""
    You are Cypher query expert working with a Kuzu graph database.
    Given the following schema and question, write a Cypher query that answers the question.
    Schema:{schema}
    Question:{question}

    Based on the the question, Cypher query, and Cypher response from the graph database, write a natural language response
    Always lowercase the movie and director names in the cypher query.

    For example:
            Question: Which movies did Aaron Sorkin direct?
            Output:
              MATCH (d:Director)<-[r1:DIRECTED_BY]-(m:Movie) WHERE lower(d.Director) = lower('Aaron Sorkin') RETURN m.Series_Title AS movie_directed

            Question: Who all were cast in the movie dunkirk?
            Output:
              MATCH (m:Movie {{Series_Title: lower('Dunkirk)}})<-[:STARRED_IN]-(s1:Star1) MATCH (m:Movie {{Series_Title: lower('Dunkirk')}})<-[:SECOND_LEAD_IN]-(s2:Star2) MATCH (m:Movie {{Series_Title: lower('Dunkirk')}})<-[:SUPPORTING_ACTOR_IN]-(s3:Star3) MATCH (m:Movie {{Series_Title: lower('Dunkirk')}})<-[:SECOND_SUPPORTING_ACTOR_IN]-(s4:Star4) RETURN s1.Star1 AS Star, s2.Star2 AS Second_lead, s3.Star3 AS Supporting_actor, s4.Star4 AS Second_supporting_actor
            
    """
)

def graphRagQA(query):
    # Create the KuzuQAChain with verbosity enabled to see the generated Cypher queries
    chain_kuzuQAChain = KuzuQAChain.from_llm(
        llm =llm_gemini,
        graph=graph,
        verbose=True,
        allow_dangerous_requests=True,
        cypher_prompt=cypher_prompt_template_kuzuQAChain,
        return_intermediate_steps=True
    )
    result=chain_kuzuQAChain.invoke(query)
    return result
    
