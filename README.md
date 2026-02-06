# The Board 

**The Board** is a multi-agent AI chat application built with **FastAPI**, **CrewAI**, and a lightweight JavaScript frontend.  
It allows users to have structured conversations with an AI “board” made up of multiple agents (Generator, Refiner, Translator), with switchable perspectives such as **supporter** or **contrarian**.

The app supports persistent chat sessions, message history, and real-time perspective changes.

---

## Features

- **Multi-agent reasoning** using CrewAI
- **Sequential response pipeline** (generate → refine → translate)
- **Dynamic perspectives** (e.g. supporter, contrarian)
- **Session-based chat history** stored in a database
- **FastAPI backend** with REST endpoints
- **Vanilla JavaScript frontend**
- CORS-enabled API for easy frontend integration

---

## Tech Stack

**Backend**
- Python
- FastAPI
- CrewAI
- SQLite (via custom DB utilities)
- Pydantic

**Frontend**
- HTML / CSS
- Vanilla JavaScript
- Fetch API
- LocalStorage for session persistence

---
