# =============================================================================
# Marketing Assistant AI - Main Application (Cohere + HF Version)
# =============================================================================
# Cohere is used for embeddings/rerank (API key required).
#
# Tech Stack:
# - Cohere for embeddings (API)
# - FAISS for vector search (local)
# - Cohere for re-ranking (API)
# - Hugging Face Transformers for LLM (local)
#
# To run: python main.py
# API Docs: http://localhost:8000/docs
# =============================================================================

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from backend.config import settings
from backend.routers import generation_router, generation_public_router, training_data_router

# =============================================================================
# Logging Configuration
# =============================================================================

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


# =============================================================================
# Application Lifespan
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # Startup
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name}")
    logger.info("=" * 60)
    logger.info("Cohere API is required for embeddings and re-ranking.")
    logger.info("=" * 60)
    logger.info(f"Embedding model: {settings.cohere_embed_model}")
    logger.info(f"LLM model: {settings.huggingface_model}")
    logger.info(f"Re-rank model: {settings.cohere_rerank_model}")
    logger.info("=" * 60)
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# =============================================================================
# FastAPI Application
# =============================================================================

app = FastAPI(
    title=settings.app_name,
    description="""
## Marketing Assistant AI

AI-powered marketing copy generation aligned with **Adriana James' brand voice**.

**Cohere API key required** for embeddings and re-ranking.

### Tech Stack
- **Embeddings**: Cohere (API)
- **Vector DB**: FAISS (local)
- **Re-ranking**: Cohere (API)
- **LLM**: Hugging Face Transformers (local)

### Quick Start
1. Seed sample data: `POST /api/v1/training-data/seed`
2. Generate content: `POST /generate-copy`
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Exception Handler
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
        }
    )


# =============================================================================
# Routers
# =============================================================================

app.include_router(generation_router)
app.include_router(generation_public_router)
app.include_router(training_data_router)


# =============================================================================
# Root & UI Endpoints
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """API information."""
    return {
        "name": settings.app_name,
        "version": "1.0.0",
        "description": "AI-powered marketing copy generation",
        "stack": {
            "embeddings": f"Cohere ({settings.cohere_embed_model})",
            "vector_db": "FAISS",
            "reranking": f"Cohere ({settings.cohere_rerank_model})",
            "llm": f"Hugging Face ({settings.huggingface_model})"
        },
        "docs": "/docs",
        "cohere_required": True,
        "endpoints": {
            "generate_copy": "/generate-copy",
            "generate": "/api/v1/generate",
            "refine": "/api/v1/generate/refine",
            "content_types": "/api/v1/generate/content-types",
            "training_data": "/api/v1/training-data",
            "training_data_seed": "/api/v1/training-data/seed"
        }
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check."""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "embeddings": "cohere",
            "vector_store": "local", 
            "reranker": "cohere",
            "llm": "local (huggingface)"
        },
        "note": "Cohere API key required for embeddings and reranking."
    }


@app.get("/playground", response_class=HTMLResponse, tags=["UI"])
async def playground():
    """
    Minimal in-browser UI for trying the marketing assistant.
    
    This is intentionally lightweight so it works on free CPU deployments
    (e.g. Hugging Face Spaces). It calls the public `/generate-copy` endpoint.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Marketing Assistant AI – Playground</title>
        <style>
            :root {
                color-scheme: light dark;
                --bg: #0f172a;
                --panel: #020617;
                --accent: #38bdf8;
                --accent-soft: rgba(56, 189, 248, 0.12);
                --border: #1e293b;
                --text-main: #e5e7eb;
                --text-muted: #94a3b8;
                --danger: #f97373;
                --radius: 10px;
            }
            * { box-sizing: border-box; }
            body {
                margin: 0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                background: radial-gradient(circle at top, #1e293b 0, #020617 55%, #000 100%);
                color: var(--text-main);
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                padding: 24px;
            }
            .shell {
                width: 100%;
                max-width: 980px;
                background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(15,23,42,0.98));
                border-radius: 18px;
                border: 1px solid rgba(148,163,184,0.25);
                box-shadow:
                    0 24px 80px rgba(15,23,42,0.9),
                    0 0 0 1px rgba(15,23,42,0.8);
                overflow: hidden;
            }
            .shell-header {
                padding: 14px 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: radial-gradient(circle at top left, rgba(56,189,248,0.12), transparent 55%);
                border-bottom: 1px solid var(--border);
            }
            .shell-title {
                font-size: 15px;
                font-weight: 600;
                letter-spacing: 0.03em;
                text-transform: uppercase;
                color: var(--text-muted);
            }
            .pill {
                font-size: 11px;
                padding: 4px 10px;
                border-radius: 999px;
                border: 1px solid rgba(148,163,184,0.4);
                background: rgba(15,23,42,0.7);
                color: var(--text-muted);
            }
            .content {
                display: grid;
                grid-template-columns: 1.05fr 1.1fr;
                gap: 1px;
                background: var(--border);
            }
            .panel {
                background: radial-gradient(circle at top left, rgba(56,189,248,0.06), rgba(15,23,42,0.96));
                padding: 20px 22px 18px;
            }
            .panel + .panel {
                background: radial-gradient(circle at top right, rgba(56,189,248,0.08), rgba(15,23,42,0.96));
            }
            .field-label {
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: var(--text-muted);
                margin-bottom: 6px;
            }
            .badge-row {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-bottom: 10px;
            }
            .badge {
                font-size: 11px;
                padding: 3px 8px;
                border-radius: 999px;
                border: 1px solid rgba(148,163,184,0.3);
                color: var(--text-muted);
            }
            label {
                display: block;
                margin-top: 10px;
                margin-bottom: 4px;
                font-size: 13px;
                color: var(--text-main);
            }
            select, textarea, input[type="text"] {
                width: 100%;
                border-radius: 10px;
                border: 1px solid var(--border);
                background: rgba(15,23,42,0.9);
                color: var(--text-main);
                padding: 8px 10px;
                font-size: 13px;
                outline: none;
            }
            textarea {
                min-height: 110px;
                resize: vertical;
            }
            select:focus, textarea:focus, input[type="text"]:focus {
                border-color: rgba(56,189,248,0.7);
                box-shadow: 0 0 0 1px rgba(56,189,248,0.25);
            }
            .btn-row {
                margin-top: 12px;
                display: flex;
                justify-content: flex-end;
                gap: 8px;
            }
            button {
                border-radius: 999px;
                padding: 8px 18px;
                border: 1px solid rgba(148,163,184,0.4);
                background: transparent;
                color: var(--text-main);
                font-size: 13px;
                cursor: pointer;
            }
            .btn-primary {
                border-color: rgba(56,189,248,0.7);
                background: linear-gradient(135deg, #0ea5e9, #22d3ee);
                color: #0b1120;
                font-weight: 600;
            }
            .btn-primary:disabled {
                opacity: 0.6;
                cursor: wait;
            }
            .output-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }
            .output-header span {
                font-size: 12px;
                color: var(--text-muted);
            }
            .output-box {
                border-radius: 10px;
                border: 1px solid rgba(148,163,184,0.35);
                background: radial-gradient(circle at top left, rgba(56,189,248,0.08), rgba(15,23,42,0.98));
                padding: 12px 12px 10px;
                min-height: 140px;
                max-height: 360px;
                overflow-y: auto;
                font-size: 14px;
                line-height: 1.6;
                white-space: pre-wrap;
            }
            .meta {
                margin-top: 10px;
                font-size: 11px;
                color: var(--text-muted);
            }
            .error {
                margin-top: 8px;
                font-size: 12px;
                color: var(--danger);
            }
            @media (max-width: 900px) {
                .content {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="shell">
            <div class="shell-header">
                <div class="shell-title">Marketing Assistant AI · Playground</div>
                <div class="pill">TinyLlama · RAG + Brand Voice</div>
            </div>
            <div class="content">
                <div class="panel">
                    <div class="field-label">Request</div>
                    <div class="badge-row">
                        <div class="badge">LLM: Hugging Face (local)</div>
                        <div class="badge">Embeddings: Cohere</div>
                        <div class="badge">Vector DB: FAISS</div>
                    </div>
                    <label for="contentType">Content type</label>
                    <select id="contentType">
                        <option value="campaign">Full campaign (default)</option>
                        <option value="email">Email</option>
                        <option value="social_media">Social media post</option>
                        <option value="website_copy">Website copy</option>
                        <option value="funnel_page">Funnel page</option>
                        <option value="ad_copy">Ad copy</option>
                        <option value="blog_post">Blog post</option>
                    </select>
                    <label for="prompt">Prompt</label>
                    <textarea id="prompt" placeholder="e.g., Create a launch email for my new 6-week mindset program for women entrepreneurs."></textarea>
                    <label for="audience">Target audience (optional)</label>
                    <input id="audience" type="text" placeholder="e.g., Women entrepreneurs in their 30s juggling business and family" />
                    <label for="keyPoints">Key points (comma separated, optional)</label>
                    <input id="keyPoints" type="text" placeholder="e.g., 6-week program, live calls, limited spots" />
                    <div class="btn-row">
                        <button type="button" id="clearBtn">Clear</button>
                        <button type="button" class="btn-primary" id="generateBtn">Generate copy</button>
                    </div>
                    <div class="error" id="error"></div>
                </div>
                <div class="panel">
                    <div class="output-header">
                        <div class="field-label" style="margin: 0;">Generated Copy</div>
                        <span id="statusLabel">Idle</span>
                    </div>
                    <div class="output-box" id="output">
                        Type a prompt on the left and click <strong>Generate copy</strong>.
                    </div>
                    <div class="meta" id="meta"></div>
                </div>
            </div>
        </div>
        <script>
            async function generate() {
                const promptEl = document.getElementById("prompt");
                const typeEl = document.getElementById("contentType");
                const audienceEl = document.getElementById("audience");
                const keyPointsEl = document.getElementById("keyPoints");
                const outputEl = document.getElementById("output");
                const metaEl = document.getElementById("meta");
                const errEl = document.getElementById("error");
                const statusEl = document.getElementById("statusLabel");
                const btn = document.getElementById("generateBtn");
                
                const prompt = promptEl.value.trim();
                if (!prompt) {
                    errEl.textContent = "Please enter a prompt first.";
                    return;
                }
                errEl.textContent = "";
                statusEl.textContent = "Generating...";
                btn.disabled = true;
                
                const keyPointsRaw = keyPointsEl.value.trim();
                const keyPoints = keyPointsRaw
                    ? keyPointsRaw.split(",").map(x => x.trim()).filter(Boolean)
                    : [];
                
                const payload = {
                    prompt: prompt,
                    content_type: typeEl.value,
                    target_audience: audienceEl.value.trim() || null,
                    key_points: keyPoints,
                    tone_override: null,
                    max_length: 500
                };
                
                try {
                    const resp = await fetch("/api/v1/generate", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(payload)
                    });
                    if (!resp.ok) {
                        const data = await resp.json().catch(() => ({}));
                        throw new Error(data.detail || `Request failed with status ${resp.status}`);
                    }
                    const data = await resp.json();
                    outputEl.textContent = data.generated_content || "(no content returned)";
                    const meta = data.generation_metadata || {};
                    metaEl.textContent = `Model: ${meta.model || "unknown"} · Device: ${meta.device || "cpu"} · Temperature: ${meta.temperature ?? "n/a"}`;
                    statusEl.textContent = "Done";
                } catch (e) {
                    console.error(e);
                    errEl.textContent = e.message || "Generation failed.";
                    statusEl.textContent = "Error";
                } finally {
                    btn.disabled = false;
                }
            }
            
            document.getElementById("generateBtn").addEventListener("click", generate);
            document.getElementById("clearBtn").addEventListener("click", () => {
                document.getElementById("prompt").value = "";
                document.getElementById("audience").value = "";
                document.getElementById("keyPoints").value = "";
                document.getElementById("output").textContent = "Type a prompt on the left and click Generate copy.";
                document.getElementById("meta").textContent = "";
                document.getElementById("error").textContent = "";
                document.getElementById("statusLabel").textContent = "Idle";
            });
        </script>
    </body>
    </html>
    """


# =============================================================================
# Run directly
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.api_host, port=settings.api_port, reload=settings.debug)
