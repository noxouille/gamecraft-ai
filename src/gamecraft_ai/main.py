from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="GameCraft AI",
    description="AI-powered game development assistant",
    version="0.1.0",
)


@app.get("/")
async def root():
    return JSONResponse(content={"message": "Welcome to GameCraft AI"})


@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "healthy"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
