# Multi-Agent Travel Assistant

An AI-powered travel planning assistant built with a multi-agent architecture using 
LangGraph, orchestrating specialized agents for destination research, flight search, 
and itinerary planning — powered by Groq's LLM inference, Tavily search, and a flight 
search API.

## Overview

Planning a trip involves multiple distinct tasks — researching destinations, finding 
flights, checking weather/local info, and building a coherent itinerary. Instead of one 
monolithic prompt trying to do everything, this project breaks the problem into 
specialized agents that collaborate through a LangGraph workflow, each handling one 
part of the pipeline and passing structured results to the next.

## Architecture

The system uses **4 agents** orchestrated via LangGraph:

1. **Research Agent** — Uses the Tavily API to gather real-time information about the 
   destination (attractions, weather, local events, travel advisories).
2. **Flight Search Agent** — Queries a flight search API to find and compare flight 
   options based on user constraints (dates, budget, origin/destination).
3. **Itinerary Planner Agent** — Synthesizes research and flight data into a structured, 
   day-by-day travel itinerary tailored to user preferences.
4. **Coordinator/Orchestrator Agent** — Manages the flow between agents, handles state, 
   resolves conflicting information, and compiles the final response to the user.

Agents communicate through a shared graph state (LangGraph), allowing each agent to 
build on the previous agent's output rather than working in isolation.

## How it works

\`\`\`
User query (e.g., "Plan a 5-day trip to Bali under $1000")
        ↓
Coordinator Agent → routes task
        ↓
Research Agent (Tavily) ──┐
Flight Search Agent  ─────┼──→ Itinerary Planner Agent → Final itinerary
        ↓
Response delivered to user
\`\`\`

## Tech Stack
- **Orchestration**: LangGraph (multi-agent state graph)
- **LLM Inference**: Groq API
- **Web Search / Research**: Tavily API
- **Flight Data**: [Flight Search API name]
- **Language**: Python

## Features
- Real-time destination research via web search
- Live flight search and comparison
- Automated, structured itinerary generation
- Multi-agent coordination for more accurate, task-specific outputs than a single LLM call

## Setup

\`\`\`bash
git clone https://github.com/Parthiv0121/multi-agent-travel-assistant
cd multi-agent-travel-assistant
pip install -r requirements.txt
\`\`\`

Create a `.env` file with your API keys:
\`\`\`
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
FLIGHT_API_KEY=your_key_here
\`\`\`

## Run it
\`\`\`bash
python main.py
\`\`\`

## What I learned
- Designing multi-agent systems where each agent has a clear, single responsibility
- Managing shared state across agents using LangGraph
- Integrating multiple external APIs (search, flights, LLM inference) into one coherent pipeline
- Handling agent coordination challenges — sequencing, passing context, and merging outputs

## Future improvements
- Add a hotel search agent
- Add budget-optimization logic across flights + itinerary
- Support multi-city trip planning
- Add a simple UI (Streamlit/Next.js) for user interaction

## Screenshots / Demo
[Add a screenshot or short GIF of the assistant in action — this matters a lot for 
recruiters skimming your repo]
