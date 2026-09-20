## Prerequisites

- Python 3.12
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- Windows PowerShell or Git Bash (for commands below)

## Quick Start

1. Navigate to Project root folder.
2. Open "cmd" / "terminal"
3. Create virtual enviornment: `python -m venv venv`
4. Activate virtual enviornment: `venv\Scripts\activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Setup enviornment variables: `cp .env.example .env`
7. Run program: `python main.py`

## Features

- **Summary** – condenses the meeting transcript into a concise summary.
- **Action items** – extracts action items/next steps from the transcript.
- **Summary + action items** – returns both in a single response.
- **Sentiment analysis** – analyzes the overall tone/sentiment of the meeting.
- Intent-based routing: a supervisor agent inspects the user's request and dispatches it to the right agent (or asks for clarification if the intent is unclear).

## Project Structure

```text
agentic-ai-meeting-summary-agent/
├── .env.example
├── README.md
├── agents/
│   ├── action_agent.py
│   ├── sentiment_agent.py
│   └── summary_agent.py
├── llm/
│   └── llm_call.py
├── supervisor/
│   ├── aggregator.py
│   ├── orchestrator.py
│   └── state.py
├── formatter.py
├── graph.py
├── main.py
├── requirements.txt
└── transcript.txt
```

- **`agents/`** – task agents: `summary_agent.py` (summarization), `action_agent.py` (action items), `sentiment_agent.py` (sentiment analysis).
- **`llm/llm_call.py`** – thin wrapper around the OpenAI chat model used by all agents.
- **`supervisor/orchestrator.py`** – determines user intent and routes to the right agent(s).
- **`supervisor/aggregator.py`** – combines agent output into the final response.
- **`supervisor/state.py`** – shared LangGraph state definition.
- **`graph.py`** – wires the orchestrator, agents, and aggregator into a LangGraph workflow.
- **`formatter.py`** – formats the final response for console output.
- **`main.py`** – entry point; loads the transcript and runs the graph.
- **`.env.example`** – environment variable template.
- **`requirements.txt`** – Python dependencies.
- **`transcript.txt`** – sample input data.

## Working example

![Alt text for the image](Screenshot1.png)

## License

[MIT](./LICENSE) License © 2026-PRESENT [Parth Kansara](https://github.com/kparth01)
