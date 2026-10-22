import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi. responses import JSONResponse
from mysql.connector import Error as MySQLError

from database import executar_sql

app = FastAPI(title="API AULA REST")

@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no My SQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o BD"}
    )
def representar_produto(produto):
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "categoria": produto["categoria"],
        "preco": format(produto['preco'], ".2f"),
    }
    
@app.get("/produtos")
def listar_produtos():
    sql = "SELECT id, nome, categoria, preco FROM produtos"
    produtos = executar_sql(sql)
    
    return {
        "dados": [representar_produto(produto) for produto in produtos],
        "didatica": {"sql": sql, "parametros": []},
    }
