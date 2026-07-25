# Agentic

A Python framework for building intelligent AI agents powered by OpenAI Agents SDK. This repo demonstrates how to create, configure, and orchestrate AI agents with tools, memory management, and multi-agent coordination.

## Overview

**Agentic** provides a practical implementation of agent-based systems, showcasing key concepts like:
- **Tool Integration**: Agents can use custom tools to interact with external APIs and services
- **Memory Management**: Persistent conversation history with automatic summarization for long interactions
- **Agent Orchestration**: Multi-agent systems that work together to solve complex problems
- **Contextual Awareness**: User context and preferences maintained throughout agent interactions

## Features

### 1. **Travel Assistant** (`agentic.py`)
A single-agent system that helps users plan trips by providing:
- Real-time weather information for cities
- Restaurant recommendations by cuisine type
- Flight availability and pricing

### 2. **Persistent Memory System** (`memory.py`)
Demonstrates advanced memory management with:
- SQLite-backed persistent sessions
- User context preservation (premium status, user facts)
- Automatic conversation summarization when history grows
- Dynamic agent instructions based on factual user context

### 3. **Agent Orchestration** (`orchestration.py`)
Shows multi-agent patterns with:
- Specialized agents (Weather Agent, Flight Agent)
- Travel Coordinator Agent that can delegate tasks via handoffs
- But Note in this code the handoffs are commented off becuase for a simple example like this one they do not work

### 4. **Practice Examples** (`practice.py`)
Additional examples and experimentation scripts for learning agent patterns.

## Requirements
See `requirements.txt` for the complete dependency list.

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Thabo-Dladla/Agentic.git
cd Agentic
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file in the root directory
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Running the Examples

**Travel Assistant:**
```bash
python agentic.py
```
Interact with the travel assistant to ask about weather, restaurants, and flights.

**Memory & Context Example:**
```bash
python memory.py
```
Demonstrates how agents maintain user context and persistent memory across conversations.

**Agent Orchestration:**
```bash
python orchestration.py
```
Shows how specialized agents work together to handle travel-related queries.

## Project Structure

```
Agentic/
├── agentic.py           # Travel assistant with tool integration
├── memory.py            # Persistent memory and user context management
├── orchestration.py     # Multi-agent coordination patterns
├── practice.py          # Practice examples and experimentation
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Core Concepts

### Agents
Agents are AI-powered entities that can:
- Receive user instructions
- Use tools to gather information
- Maintain conversation history
- Make decisions based on context

### Tools
Tools are functions that agents can call to perform actions:
```python
@function_tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # Implementation
```

### Sessions
Sessions maintain conversation history and can be persisted using SQLite:
```python
session = SQLiteSession("user_id_conversation")
result = Runner.run_sync(agent, user_input, session=session, context=user_context)
```

### Context
User-specific information that agents can access:
```python
@dataclass
class UserContext:
    user_id: str
    is_premium: bool
    user_facts: dict
```

## Usage Examples

### Basic Agent Interaction
```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city} is sunny."

agent = Agent(
    name="WeatherBot",
    instructions="You are a helpful weather assistant.",
    tools=[get_weather]
)

result = Runner.run_sync(agent, "What's the weather in London?")
print(result.final_output)
```

### Agent with Persistent Memory
```python
session = SQLiteSession("conversation_123")
context = UserContext(user_id="user_123", is_premium=True, user_facts={})

result = Runner.run_sync(agent, "Hi, I'm Alice", session=session, context=context)
print(result.final_output)
```

## How It Works

1. **User Input**: User provides a query to the agent
2. **Tool Selection**: Agent decides which tools are needed
3. **Tool Execution**: Tools are called to gather information
4. **Response Generation**: Agent synthesizes responses based on tool results
5. **Memory Update**: Conversation is saved to persistent storage
6. **Context Preservation**: User context is updated for future interactions

## Key Features Explained

### Automatic Summarization
When conversation history exceeds 20 messages,the system:
- Summarizes earlier conversations using GPT-4
- Preserves recent interactions for context
- Maintains conversation continuity

### Premium User Features
- Access to advanced analytics data
- Priority support (in demonstration)
- Can be extended with custom features

### Tool Integration
Agents seamlessly integrate with external APIs:
- Weather API (wttr.in)
- Restaurant data (placeholder for real APIs)
- Flight information (placeholder for real booking systems)

## Troubleshooting

**API Key Issues:**
- Ensure `OPENAI_API_KEY` is set in your `.env` file
- Verify your API key has proper permissions

**Import Errors:**
- Run `pip install -r requirements.txt` to ensure all dependencies are installed
- Verify you're using Python 3.8 or higher

**Session Errors:**
- Check that the SQLite database file has write permissions
- Ensure the session directory exists

## Learning Resources

This project demonstrates:
- Building AI agents with OpenAI Agents SDK
- Tool use and function calling
- Session management, memory persistence and context-aware conversations
- Multi-agent systems and orchestration
- Best practices for agent development

---
