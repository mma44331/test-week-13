import uvicorn
from fastapi import FastAPI, UploadFile
import db
import pandas as pd
from models import ThreatOut


app = FastAPI()


@app.post("/top-threats")
def get_file_threats(file:UploadFile):
    file = pd.read_csv(file.file)
    return validtion_of_file(file)

def validtion_of_file(file):
    new_file = []
    file = file.sort_values(by="danger_rate",ascending=False).head(5)
    file = file[["name", "location", "danger_rate"]]
    for row in file.to_dict(orient="records"):
        threat = ThreatOut(
            name=row["name"],
            location=row["location"],
            danger_rate=row["danger_rate"]
        )
        new_file.append(threat.dict())
    count = len(new_file)
    data = {f"count":count,"top":new_file}
    return send_to_db(data)

def send_to_db(data:dict):
    mongo = db.Threads()
    mongo.create_new_threat(data)
    data = mongo.get_threats()
    return data



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost",port=8000 , reload=True)
