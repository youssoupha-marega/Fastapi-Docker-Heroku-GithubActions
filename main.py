## Executer la commande suivante pour voir l'application : uvicorn main:app --reload --host 0.0.0.0 --port 8000
### l'app va etre disponible via le navigateur http://127.0.0.1:8000/
## Pour la documentation l'app disponible http://127.0.0.1:8000/docs


from fastapi import FastAPI
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def index():
    return{"details":"hello Mise à jour okay, world!"}
    
    
    
# ✅ Groupe d'endpoints "Utilisateurs"
@app.get("/users", tags=["Utilisateurs"])
def get_users():
    return {"users": ["Alice", "Bob", "Charlie"]}

@app.get("/users/{user_id}", tags=["Utilisateurs"])
def get_user(user_id: int):
    return {"user_id": user_id, "name": "Utilisateur " + str(user_id)}


# ✅ Groupe d'endpoints "Calculatrice"
@app.get("/addition", tags=["Calculatrice"])
def addition(x: float, y: float):
    return {"operation": "addition", "x": x, "y": y, "resultat": x + y}

@app.get("/soustraction", tags=["Calculatrice"])
def soustraction(x: float, y: float):
    return {"operation": "soustraction", "x": x, "y": y, "resultat": x - y}

@app.get("/multiplication", tags=["Calculatrice"])
def multiplication(x: float, y: float):
    return {"operation": "multiplication", "x": x, "y": y, "resultat": x * y}

@app.get("/division", tags=["Calculatrice"])
def division(x: float, y: float):
    if y == 0:
        return {"error": "Division par zéro impossible"}
    return {"operation": "division", "x": x, "y": y, "resultat": x / y}    





# ✅ Groupe d'endpoints "Presentation"
@app.get("/presente toi", tags=["Presentation de mon petit frere chérie Moussa Marega"])
def presente_toi(nom: str, prenom: str, date_naissance: str, profession: str, salaire: int):
    """
    Cette fonction retourne une présentation formatée avec l'âge calculé.
    - `date_naissance` doit être au format "19-02-1997".
    """

    # ✅ Convertir la date de naissance en objet datetime
    try:
        date_naissance_obj = datetime.strptime(date_naissance, "%d-%m-%Y")
    except ValueError:
        return {"error": "Format de date invalide. Utilisez JJ-MM-AAAA (ex: 19-02-1997)"}

    # ✅ Calculer l'âge
    aujourd_hui = datetime.today()
    age = aujourd_hui.year - date_naissance_obj.year - ((aujourd_hui.month, aujourd_hui.day) < (date_naissance_obj.month, date_naissance_obj.day))

    # ✅ Construire le message de réponse
    response = f"Bonjour, je m'appelle {prenom} {nom}. Je suis né(e) le {date_naissance} et j'ai {age} ans. "
    response += f"Je travaille comme {profession} et mon salaire est de {salaire} euros."

    return {"Mon message subliminale": response}

    