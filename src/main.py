import uvicorn
from fastapi import FastAPI


app = FastAPI()


@app.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
