from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return{"details":"hello Misa jour okay, world!"}
    
    
## Executer la commande suivante pour voir l'application : uvicorn main:app --reload --host 0.0.0.0 --port 8000
### l'app va etre disponible via le navigateur http://127.0.0.1:8000/
## Pour la documentation l'app disponible http://127.0.0.1:8000/docs

