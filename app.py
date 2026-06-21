from fastapi import FastAPI
from fastapi import Query
from engine import investigate_incident
from rca_engine import generate
from timeline_engine import generate_timeline
from recommendation_engine import generate_recommendations
from coral_agent import investigate


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Incident Investigation Agent Running"}



@app.get("/incident")
def incident():
    return investigate_incident()

@app.get("/rca")
def rca():
    return generate()

@app.get("/timeline")
def timeline():
    return generate_timeline()

@app.get("/recommendations")
def recommendations():
    return generate_recommendations()


@app.get("/coral")
def coral(
    owner: str = Query(...),
    repo: str = Query(...)
):
    return investigate(owner,repo)

