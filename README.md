# AriaChat

AriaChat is a case study exploring how **intelligent capabilities can be integrated into future Excite! Innovation products**, with a focus on AI integration, developer productivity, and Backend–AI/ML collaboration.

## Case Study Focus

The case study examines how AI can be introduced into product development while exploring the technical architecture, engineering workflows, and collaboration required to build AI-powered experiences.

- AI integration into product experiences
- AI application architecture
- Developer experience and productivity
- Backend and AI/ML collaboration

## Capabilities

AriaChat demonstrates practical conversational AI capabilities, including natural interaction, context-aware responses, persistent conversations, automatic titles, message regeneration, AI-generated greetings, and memory of relevant user context.

## System Architecture & Project Structure

The core principle was to establish a **modular architecture and project structure**, keeping the frontend, backend, and AI components clearly separated.

AriaChat connects the frontend, Django API, AI services, Google ADK, Ollama, and Llama 3.2 3B in distinct layers, making the system easier to develop, maintain, and evolve.

## Outcomes & Next Steps

Progressively integrate the research findings into **Boltshift’s customer experience and vendor back office**, introducing AI-powered features as product and engineering teams establish the required **data hygiene, quality, and readiness** throughout the roadmap.


# Test the project on your machine

## Docker Setup

Run AriaChat locally with Docker:
Download and install [**Docker Desktop**](https://www.docker.com/products/docker-desktop/)

```bash
git clone https://github.com/paulXmbingu/aria_chatbot
cd aria_chatbot
docker compose up --build
http://localhost:8000
```


## uv Setup

Install dependencies with **uv**:
Download and install [**uv**](https://docs.astral.sh/uv/getting-started/installation/)

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
http://localhost:8000
```