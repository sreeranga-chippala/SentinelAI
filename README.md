# SentinelAI: Multi-Agent Disaster Response Coordination System

## Overview

Natural disasters such as floods, earthquakes, cyclones, and large-scale accidents require emergency responders to make critical decisions under severe time pressure. These decisions depend on information from multiple sources, including weather conditions, road accessibility, population density, and nearby medical facilities. Collecting, validating, and combining this information manually can be slow, fragmented, and prone to human error, delaying rescue operations when every minute matters.

**SentinelAI** is an AI-powered **multi-agent disaster response coordination system** that automates this process by orchestrating specialized AI agents to gather real-time situational intelligence and generate coordinated disaster response plans. Instead of relying on a single general-purpose agent, SentinelAI assigns dedicated responsibilities to specialized agents, enabling modular, scalable, and reliable decision-making.

---

# Problem Statement

Emergency response teams often need to answer several critical questions simultaneously:

- What are the current weather conditions?
- Which roads remain accessible for rescue operations?
- How many people are likely to be affected?
- Which hospitals are closest and capable of receiving patients?
- How should rescue teams and emergency resources be allocated?
- How should emergency information be communicated to the public?

Answering these questions quickly requires integrating multiple independent information sources. Traditional systems usually depend on manual coordination or isolated software tools, making it difficult to build a unified operational picture during rapidly evolving disasters.

---

# Solution

SentinelAI addresses this challenge using a **multi-agent architecture built with Google's Agent Development Kit (ADK)**.

Each specialized agent focuses on a single domain of expertise:

- **Weather Agent** retrieves current weather information.
- **Traffic Agent** analyzes road conditions and rescue routes.
- **Population Agent** gathers demographic information about affected areas.
- **Hospital Agent** identifies nearby hospitals and emergency medical facilities.

Each agent interacts with its respective **Model Context Protocol (MCP) Server**, allowing external services and tools to be accessed through standardized interfaces.

Once all situational intelligence has been collected, a centralized **Mission Planner Agent** performs reasoning over the combined information and produces a comprehensive disaster response strategy.

The generated response includes:

- Priority assessment of affected areas
- Resource allocation recommendations
- Rescue mission planning
- Hospital assignment
- Public emergency alerts
- SMS notifications
- Radio announcements
- Television announcements
- Social media alerts

---

# System Architecture

SentinelAI follows a modular orchestration architecture designed for scalability and maintainability.

```text
                    Streamlit Dashboard
                           │
                    Disaster Location
                           │
                    Coordinator
                           │
       ┌────────────┬────────────┬────────────┬────────────┐
       │            │            │            │
 Weather MCP   Traffic MCP Population MCP Hospital MCP
       │            │            │            │
       └────────────┴────────────┴────────────┘
                           │
                     WorldState
                           │
                  Mission Planner Agent
                           │
        Priority • Allocation • Missions • Alerts
                           │
    Commander • Hospital • Rescue • Public Dashboards
```

The **Coordinator** orchestrates the execution of all agents while the **WorldState** acts as a centralized shared state that stores system inputs, generated knowledge, decisions, metrics, logs, and historical snapshots. This separation of responsibilities ensures that agents remain independent and stateless while maintaining a consistent global view of the disaster response process.

---

# Key Technologies

SentinelAI is built using:

- Python
- Google Agent Development Kit (ADK)
- Google Gemini
- Model Context Protocol (MCP)
- Streamlit
- Asynchronous Programming (asyncio)
- Environment-based configuration using `.env`

The system also implements retry mechanisms and reusable agent sessions to improve reliability while reducing unnecessary initialization overhead.

---

# Key Features

- Multi-agent disaster response workflow
- Parallel execution of specialized intelligence agents
- MCP-based integration with external data providers
- Centralized mission planning using a reasoning agent
- Shared WorldState for coordinated decision making
- Real-time dashboards for multiple stakeholders
- Resource allocation and rescue mission generation
- Automated public communication across multiple channels
- Modular architecture designed for future expansion

---

# Innovation

Unlike traditional chatbot-style disaster assistants, SentinelAI separates **information gathering** from **decision making**.

Specialized MCP-powered agents independently collect trusted domain-specific information, while a single planning agent synthesizes these inputs into coordinated operational decisions. This architecture reduces hallucinations, improves modularity, minimizes reasoning costs, and allows additional agents or external services to be integrated with minimal changes to the overall system.

---

# Impact

SentinelAI demonstrates how AI agents can support emergency management by transforming distributed situational intelligence into coordinated operational plans. The architecture is applicable to disaster response, emergency command centers, humanitarian relief operations, and other public safety scenarios where rapid, reliable, and explainable coordination is essential.

By combining **Google ADK**, **MCP Servers**, **multi-agent orchestration**, and a centralized planning workflow, SentinelAI showcases how modern AI agents can be deployed to solve real-world humanitarian challenges efficiently and responsibly.