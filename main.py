import os
from typing import Annotated,TypedDict
import operator

import psycopg
from langgraph.graph import StateGraph, START,END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (AnyMessage, HumanMessage, AIMessage, SystemMessage)

from langchain_groq import ChatGroq

#create by my own
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flight


from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
  model="llama-3.3-70b-versatile",
  api_key=os.getenv("GROQ_API_KEY"),

)

#Database connection
DATABASE_URL = os.getenv("DATABASE_URL")

#create state in langgraph

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int


## Creating Flight Agent

def flight_agent(state: TravelState):
  query = state["user_query"]
  flight_data = search_flight(query)
  return{
    "flight_results": flight_data,
    "messages": [
      AIMessage(content=f"Flight results fetched for query: {query}")
    ],
    "llm_calls": state.get("llm_calls", 0) + 1
  }



## Creating Hotel Agent

def hotel_agent(state: TravelState):
    query = f"Best hotel for {state['user_query']}"
    hotel_data = tavily_search(query)

    return {
        "hotel_results": hotel_data,
        "messages": [
            AIMessage(content=f"Hotel results fetched for query: {query}")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


##Creating Itinerary Agent

def itinerary_agent(state: TravelState):
  prompt = f""" 
  Create a travel ininerary.
  User Query: {state["user_query"]}

  Flight Results: {state["flight_results"]}

  Hotel Results: {state["hotel_results"]}
   """

  response = llm.invoke([
    SystemMessage(content="You are a expert travel assistant that creates travel itineraries based on user queries, flight results, and hotel results."),
    HumanMessage(content=prompt)  
   ])


##Update the state with the itinerary and increment the llm_calls counter

  return {
    "itinerary": response.content,
    "messages": [response],
    "llm_calls": state.get("llm_calls", 0 )+ 1
   }


##Adding a function to save the state to the database
def final_agent(state: TravelState):
    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state["flight_results"]}

    Hotels:
    {state["hotel_results"]}

    Itinerary:
    {state["itinerary"]}
    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

##Creating the Graph

graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

## Creating the connections between the nodes

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)



#import psycopg
#from langgraph.checkpoint.postgres import PostgresSaver

_conn = psycopg.connect(DATABASE_URL, autocommit=True)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
  config = {
    "configurable": {
      "thread_id": "user_aarohi"
    }
  }

  user_input = input("Enter travel request:")

result = app.invoke(
    {
        "messages": [HumanMessage(content=user_input)],
        "user_query": user_input,
        "flight_results": "",
        "hotel_results": "",
        "itinerary": "",
        "llm_calls": 0,
    },
    
    config=config
)
print(result)







