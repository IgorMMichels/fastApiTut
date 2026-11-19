import logging

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API PETSHOP")


@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o BD"},
    )


def representar_tutor(tutor):
    return {
        "id": tutor["id"],
        "nome": tutor["nome"],
        "telefone": tutor["telefone"],
        "email": tutor["email"],
    }


def representar_pet(pet):
    nascimento = pet["data_nascimento"]
    return {
        "id": pet["id"],
        "nome": pet["nome"],
        "especie": pet["especie"],
        "raca": pet["raca"],
        "data_nascimento": nascimento.isoformat() if nascimento else None,
        "tutor_id": pet["tutor_id"],
    }


SQL_TUTORES = "SELECT id, nome, telefone, email FROM tutores"
SQL_PETS = "SELECT id, nome, especie, raca, data_nascimento, tutor_id FROM pets"


@app.get("/listartutores")
def listar_tutores():
    tutores = executar_sql(SQL_TUTORES)
    return {
        "dados": [representar_tutor(t) for t in tutores],
        "didatica": {"sql": SQL_TUTORES, "parametros": []},
    }


@app.get("/listarpets")
def listar_pets():
    pets = executar_sql(SQL_PETS)
    return {
        "dados": [representar_pet(p) for p in pets],
        "didatica": {"sql": SQL_PETS, "parametros": []},
    }


@app.get("/consultartutor/{id}")
def consultar_tutor(id: int = Path(gt=0)):
    sql = SQL_TUTORES + " WHERE id = %s"
    tutores = executar_sql(sql, (id,))
    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado")
    return {
        "dados": representar_tutor(tutores[0]),
        "didatica": {"sql": sql, "parametros": [id]},
    }


@app.get("/consultarpet/{id}")
def consultar_pet(id: int = Path(gt=0)):
    sql = SQL_PETS + " WHERE id = %s"
    pets = executar_sql(sql, (id,))
    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado")
    return {
        "dados": representar_pet(pets[0]),
        "didatica": {"sql": sql, "parametros": [id]},
    }