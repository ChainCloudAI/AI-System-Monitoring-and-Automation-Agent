# AI-System-Monitoring-and-Automation-Agent
A stateful AI-assisted system monitoring and automation agent that collects system metrics, recommends and executes maintenance actions, and visualizes system activity through a real-time dashboard.

---

## Overview

This project integrates system monitoring, LLM-based decision making, automated execution, and persistent memory into a unified workflow.

The agent evaluates system conditions, generates actions based on current state and past behavior, executes predefined tools, and records outcomes for future decision-making.

---

## Core Architecture

The system follows a structured agent loop:

Observe → Reason → Plan → Execute → Record → Repeat

### Components

#### Monitoring Layer
Collects real-time system metrics:
- CPU usage
- Memory usage
- Disk usage

#### Decision Layer (LLM Integration)
- Uses a locally hosted LLM via Ollama
- Interprets system state and activity history
- Produces structured outputs:
  - detected issues
  - recommended actions
  - reasoning

#### Tool Layer
Executes system-level operations:
- Process inspection
- Network diagnostics
- Memory and disk cleanup (simulated)
- Screenshot detection and deletion (real file operations)

All tools are constrained to a predefined safe set.

#### Memory Layer
- Stores action history using a persistent JSON file
- Enables stateful behavior across runs
- Reduces redundant actions

#### Controller
Coordinates the workflow:
- collects system metrics
- sends structured input to the LLM
- executes recommended actions
- records results for future use

#### Dashboard (Streamlit)
Provides a user interface with:
- real-time system metrics
- alerts
- action summaries
- screenshot analytics
- historical activity

---

## Features

- Multi-step action planning
- Persistent memory across executions
- Real system interaction (file system operations)
- Safe execution with constrained tools
- Real-time dashboard using Streamlit
- Action logging and analytics

---

## Example Workflow

1. Collect system metrics
2. Load previous actions
3. Send system state to LLM
4. Receive prioritized actions
5. Execute actions sequentially
6. Record actions and outcomes
7. Repeat with updated state on next run

---

## Running the Project

Run the agent:
```
python3 test_cpu.py
```

Run the dashboard:
```
streamlit run app.py
```

---

## Project Structure

```
agent/
    analyzer.py
    memory.py
    agent_memory.json

tools/
    system_tools.py

app.py
test_cpu.py
screenshot_log.json
```

---

## Limitations

- LLM outputs are non-deterministic
- Limited toolset with predefined actions
- No asynchronous execution
- Uses JSON for persistence instead of a database
- Designed for single-machine operation

---

## Future Improvements

- Replace JSON with a database (e.g., SQLite or PostgreSQL)
- Add asynchronous execution
- Implement REST API layer
- Add automated tests
- Containerize using Docker
- Expand toolset (service management, networking tools)
- Enhance UI with real-time logs and graphs

---

## Summary

This project demonstrates a modular system that integrates monitoring, AI-assisted reasoning, execution, persistence, and visualization into a cohesive workflow. The emphasis is on system design and interaction between components rather than isolated functionality.

---

## Author

Huy Truong
