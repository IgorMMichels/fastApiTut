import logging

from fastapi import FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API Petshop")

SQL_TUTORES = "SELECT id, nome, telefone, email FROM tutores"
SQL_PETS = "SELECT id, nome, especie, raca, data_nascimento, tutor_id FROM pets"


@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
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


@app.get("/listartutores")
def listar_tutores():
    sql = SQL_TUTORES + " ORDER BY id"
    tutores = executar_sql(sql)

    return {
        "dados": [representar_tutor(tutor) for tutor in tutores],
        "sintaxesql": {"sql": sql, "parametros": []},
    }


@app.get("/listarpets")
def listar_pets():
    sql = SQL_PETS + " ORDER BY id"
    pets = executar_sql(sql)

    return {
        "dados": [representar_pet(pet) for pet in pets],
        "sintaxesql": {"sql": sql, "parametros": []},
    }


@app.get("/consultartutor/{tutor_id}")
def consultar_tutor(tutor_id: int = Path(gt=0)):
    sql = SQL_TUTORES + " WHERE id = %s"
    parametros = (tutor_id,)
    tutores = executar_sql(sql, parametros)

    if not tutores:
        raise HTTPException(status_code=404, detail="Tutor não encontrado.")

    return {
        "dados": representar_tutor(tutores[0]),
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }


@app.get("/consultarpet/{pet_id}")
def consultar_pet(pet_id: int = Path(gt=0)):
    sql = SQL_PETS + " WHERE id = %s"
    parametros = (pet_id,)
    pets = executar_sql(sql, parametros)

    if not pets:
        raise HTTPException(status_code=404, detail="Pet não encontrado.")

    return {
        "dados": representar_pet(pets[0]),
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }
