import uvicorn
from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/healthcheck")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    config = uvicorn.Config(
        "main:create_app",
        reload=True,
        factory=True,
    )
    server = uvicorn.Server(config)
    server.run()
