from typing import Dict

import uvicorn
from fastapi import FastAPI

from city_pollution.routers import pollution, city

app = FastAPI()

app.include_router(pollution.router)
app.include_router(city.router)


@app.get("/", operation_id="homepage", summary="Home Page")
def homepage() -> Dict[str, str]:
    return {"message": "Ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
