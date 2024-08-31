from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import agents
from pyzzz import agents
from pyzzz import weapons
from pyzzz import model
from pyzzz.server.calc_impl import calc


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "hello world"


@app.get("/list_agents")
def list_agents():
    return agents.list_agents()


@app.get("/list_weapons")
def list_weapons():
    return weapons.list_weapons()


@app.put("/calc")
def read_calc(data: model.CalcInput):
    return calc(data)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("pyzzz.server.main:app", port=5000, log_level="debug", reload=True)
