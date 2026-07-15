# HeadSpace AI

HeadSpace AI is an industry-grade, AI-powered Mental Health Companion. It provides personalized wellness tracking, journaling, and conversational support using advanced machine learning and large language models.

**Disclaimer:** *HeadSpace AI is designed for supportive wellness tracking and guidance. It is not a substitute for professional mental health therapy or medical diagnosis. If you are experiencing a crisis, please reach out to emergency services immediately.*

## Features

- **AI Therapist Chat**: Context-aware multi-turn conversations.
- **Emotion Detection**: Custom ML classifier predicting emotions from journal entries and messages.
- **Mood Tracking & Analytics**: Visualize mood trends and emotional well-being over time.
- **RAG for Mental Health Resources**: Retrieve contextual information from curated wellness documents.
- **Crisis Detection**: Immediate safety messaging and routing to emergency resources.
- **ML Benchmarking Pipeline**: End-to-end framework for evaluating Embedding vs TF-IDF models, registered automatically via MLflow Model Registry.
- **AI Orchestration Architecture**: LangGraph-based `StateGraph` abstracting all agent intelligence.
- **Production Memory Subsystem**: Integrated Short-Term, Long-Term (Postgres SQL), Summary, and Semantic memory coordinator with automated retrieval ranking and context compression.
- **Prompt & LLM Management**: Strict PromptRegistry and ContextBuilder decoupling hardcoded strings from logic, paired with a resilient Gemini provider featuring automated retries and Pydantic-based OutputParsing.
- **Agentic Hybrid RAG**: Advanced Qdrant-based retrieval pipeline utilizing Dense+Sparse fusion, Query Rewriting, Cross-Encoder reranking, and dynamic citation generation.
- **Emotion Intelligence Layer**: Native MLflow model integration powering real-time risk assessment and automated graph-level crisis routing.
- **AI Evaluation Framework**: Independent evaluation subsystem utilizing LangSmith and Ragas to track performance, latency, context precision, and planner accuracy against benchmark datasets.
- **Agent Tool Ecosystem**: Resilient async tool runtime featuring Pydantic schema validation, automatic retries, strict permissioning, and future MCP (Model Context Protocol) compatibility.
- **Journal Intelligence Engine**: Extracts structured psychological insights (emotions, themes, cognitive distortions, coping strategies) from user journal entries to power long-term AI memory and personalization.
- **Safety & Crisis Intervention Layer**: An independent subsystem that continuously monitors conversations, generates structured RiskAssessments, and overrides planner logic to intervene during emergencies with specialized safety tools.
- **Personalized Wellness Intelligence Engine**: A recommendation engine that synthesizes emotion state, journal history, long-term memory, and user goals to generate evidence-informed, actionable wellness plans validated by the Safety Layer.
- **Analytics, Insights & Explainability Platform**: A comprehensive dashboard and reporting suite that visualizes emotional trends, discovers behavioral patterns, and provides transparent explanations for every AI-generated recommendation.
- **Enterprise-Grade Infrastructure**: Fully containerized, Kubernetes-ready deployments with baked-in Prometheus/OpenTelemetry observability, Redis caching, robust connection pooling, and strict rate-limiting.

## Architecture

HeadSpace AI uses a modern, scalable tech stack:
- **Frontend**: Next.js 15, React, Tailwind CSS, shadcn/ui
- **Backend**: FastAPI (Python), SQLAlchemy
- **Databases**: PostgreSQL (Relational), Qdrant (Vector)
- **AI/ML**: LangChain, LangGraph, SentenceTransformers, Scikit-learn, XGBoost
- **MLOps**: MLflow (Experiment & Native Model Registry Tracking), SHAP (Explainability), Reproducible Metadata
- **Emotion Pipeline**: Modern MLOps architecture using `mlflow` for lifecycle management. We use an extensible `EmbeddingProvider` allowing easy swapping of state-of-the-art embedding models. MLflow natively tracks artifacts and registers the best performing runs dynamically assigning `champion` and `candidate` aliases. The backend loads the `champion` model natively via the MLflow API. All parameters are centralized in `config.py`.

For detailed architecture diagrams, refer to `docs/architecture.md`.

## Local Development Setup

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- Docker & Docker Compose

### Running the application

1. **Start the databases**:
   ```bash
   docker-compose up -d postgres qdrant
   ```

2. **Start the backend API**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

3. **Start the frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## License
MIT
