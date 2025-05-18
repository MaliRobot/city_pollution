from pathlib import Path
from typing import Dict
import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from city_pollution.routers import pollution, city
from city_pollution.config.settings import settings


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

PLOTS_DIR: Path = settings.temp_dir
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# Mount the plots directory
app.mount(settings.plots_url_base, StaticFiles(directory=PLOTS_DIR), name="plots")

app.include_router(pollution.router)
app.include_router(city.router)


@app.get("/", operation_id="homepage", summary="Home Page")
def homepage() -> Dict[str, str]:
    return {"message": "Ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
