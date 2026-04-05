# 🧠 ARIA

### Autonomous Routine Intelligence Assistant

A multi-agent AI system that integrates **tasks**, **calendar**, and **notes** via the **Model Context Protocol (MCP)** — powered by Google ADK, Gemini 2.5 Flash, and Cloud Firestore.

[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Run-4285F4?logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?logo=google&logoColor=white)](https://ai.google.dev/)
[![MCP](https://img.shields.io/badge/MCP-v1.27-00B4D8)](https://modelcontextprotocol.io/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What is ARIA?

ARIA is a **multi-agent AI assistant** that manages your daily routines — tasks, calendar events, and notes — through natural language.

> “Schedule a meeting for tomorrow at 10:00, create a task to prepare slides, and save meeting agenda notes”

ARIA handles this in one request by routing each part to the correct agent.

---

## 🏗️ Architecture

```
User → Cloud Run → FastAPI → ADK Runner → primary_agent (Gemini 2.5 Flash)
                                              ├── task_agent
                                              ├── calendar_agent
                                              └── notes_agent
                                                     │
                                              MCP Toolset (stdio)
                                                     │
                                              MCP Server (FastMCP)
                                                     │
                                              Cloud Firestore
                                           tasks | events | notes
```

---

## 🤖 Agents

- **primary_agent** → Routes requests  
- **task_agent** → Manages tasks  
- **calendar_agent** → Handles scheduling  
- **notes_agent** → Stores notes  

---

## 📁 Project Structure

```
multi-agent-system/
├── main.py
├── requirements.txt
├── Dockerfile
├── .env
├── agents/
├── mcp_server/
├── database/
├── api/
└── frontend/
```

---

## 🚀 Quick Start

### Clone
```bash
git clone https://github.com/mousomjidung/multi-agent-system.git
cd multi-agent-system
```

### Install
```bash
pip install -r requirements.txt
```

### Run
```bash
python main.py
```

---

## 🔌 API Endpoints

- `GET /` → UI  
- `POST /chat` → Chat  
- `GET /tasks` → Tasks  
- `GET /schedule` → Events  
- `GET /notes` → Notes  

---

## 🛠️ Tech Stack

- Google ADK  
- Gemini 2.5 Flash  
- FastAPI  
- Cloud Firestore  
- MCP  
