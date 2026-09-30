# AriaChat
AriaChat is a research case study exploring **AI integration in future Excite! Innovation products**. It demonstrates conversational AI through context-aware responses, persistent conversations, automatic titles, message regeneration, greetings, and memory.


### Case Study Focus

The case study's main objective was to explores how AI can be integrated into product experiences, with a focus on AI application architecture, developer experience and productivity, and collaboration between Backend and AI/ML engineering teams. UX and frontend development workflows were outside the scope of the project.

### System Architecture & Project Structure

The core principle was to establish a **modular architecture and project structure**, keeping the frontend, backend, and AI components clearly separated and easily composable.

####
![AriaChat System Architecture](https://res.cloudinary.com/excit3/image/upload/v1790744434/aria_chat_architecture_j7pahi.png)

### Outcomes & Next Steps

The case study established a foundation for AI integration, modular architecture, and Backend–AI/ML collaboration. These findings will inform the progressive integration of AI-powered capabilities into Boltshift’s customer experience and vendor back office as product and engineering teams establish the required data hygiene, quality, and readiness across the roadmap.


# Test the Project locally

- Download & Install on your os [**uv**](https://docs.astral.sh/uv/getting-started/installation/)
- Clone & open the repo.

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
http://127.0.0.1:8000
```