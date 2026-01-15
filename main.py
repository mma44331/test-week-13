import uvicorn
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
import pandas as pd
from typing import List, Dict, Any
from models import ThreatOut
# import pymongo
from python_multipart import multipart


app = FastAPI()


@app.post("/top-threats")
def get_file_threats(file:UploadFile):
    file = pd.read_csv(file.file)
    return validtion_of_file(file)

def validtion_of_file(file)-> dict:
    new_file = []
    file = file.sort_values(by="danger_rate",ascending=False).head(5)
    file = file[["name", "location", "danger_rate"]]
    for row in file.to_dict(orient="records"):
        threat = ThreatOut(
            name=row["name"],
            location=row["location"],
            danger_rate=row["danger_rate"]
        )
        new_file.append(threat)
    count = len(new_file)
    return {f"count":count,"top":new_file}




if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost",port=8000 , reload=True)
