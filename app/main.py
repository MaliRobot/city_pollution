from typing import Dict

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/", operation_id="homepage")
def homepage() -> Dict[str, str]:
    return {"message": "Ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
