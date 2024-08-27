from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return "hello world"


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("pyzzz.server.main:app", port=5000, log_level="info")


