from fastapi import FastAPI

app = FastAPI(title="minimal-api", version="0.0.1")

@app.get("/healthz")
async def health():
    return {"status": "ok"}
