from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal

from starlette.responses import FileResponse

app = FastAPI(title="Gas Price API")

app.mount("/static", StaticFiles(directory="static"), name="static")


from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# Dépendance pour récupérer la session DB (version FastAPI)
def get_db_api():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/prices/latest")
def get_latest_prices(db: Session = Depends(get_db_api)):
    query = text("""
        SELECT * FROM fuel_prices 
        GROUP BY station_name 
        HAVING MAX(sp95_updated_at)
    """)

    result = db.execute(query)

    # Transformation des résultats en liste de dictionnaires
    # .mappings() permet d'accéder aux colonnes par leur nom
    latest_prices = [dict(row) for row in result.mappings()]

    if not latest_prices:
        return {"message": "Aucune donnée trouvée"}

    return latest_prices



@app.get("/")
async def index():
    return FileResponse("index.html")


if __name__ == "__main__":
    import uvicorn
    # Pour lancer : python server.py
    uvicorn.run(app, host="0.0.0.0", port=8800)
