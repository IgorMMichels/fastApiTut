import logging

from fastapi import FastAPI, HTTPException, Path, Query, Request, Response
from fastapi.responses import JSONResponse
from mysql.connector import Error as MySQLError
from schemas import ProdutoEntrada

from database import executar_sql

app = FastAPI(title="API de produtos — Aula 1")


@app.exception_handler(MySQLError)
def erro_de_banco(request: Request, exc: MySQLError):
    logging.getLogger("uvicorn.error").error("Erro no MySQL: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Não foi possível acessar o banco de dados."},
    )


def representar_produto(produto):
    return {
        "id": produto["id"],
        "nome": produto["nome"],
        "categoria": produto["categoria"],
        "preco": format(produto["preco"], ".2f"),
    }


@app.get("/produtos")
def listar_produtos():
    sql = "SELECT id, nome, categoria, preco FROM produtos ORDER BY id"
    produtos = executar_sql(sql, escrita=False)

    return {
        "dados": [representar_produto(produto) for produto in produtos],
        "sintaxesql": {"sql": sql, "parametros": []},
    }


@app.get("/produtos/{produto_id}")
def consultar_produto(produto_id: int = Path(gt=0)):
    sql = "Select id, nome, categoria, preco FROM produtos WHERE id = %s"
    parametros = (produto_id,)
    produtos = executar_sql(sql, parametros, escrita=False)

    if not produtos:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    return {
        "dados": representar_produto(produtos[0]),
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }


@app.get("/produtos_categoria")
def listar_produtos_por_categoria(
    categoria: str | None = Query(default=None, min_length=1, max_length=50)
):
    sql = "Select id, nome, categoria, preco from produtos"
    parametros = ()

    if categoria is not None:
        sql += " WHERE categoria = %s"
        parametros = (categoria,)

    produtos = executar_sql(sql, parametros, escrita=False)

    return {
        "dados": [representar_produto(produto) for produto in produtos],
        "sintaxesql": {"sql": sql, "parametros": list(parametros)},
    }


@app.post("/produtos", status_code=201)
def criar_produto(produto: ProdutoEntrada, response: Response):
    sql = """
        INSERT INTO produtos(nome, categoria, preco)
        VALUES (%s, %s, %s)
    """.strip()

    parametros = (produto.nome, produto.categoria, produto.preco)
    resultado = executar_sql(sql, parametros, escrita=True)
    produto_id = resultado["id_gerado"]

    response.headers["Location"] = f"/produtos/{produto_id}"

    return {
        "dados": {
            "id": produto_id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": format(produto.preco, ".2f"),
        },
        "sintaxesql": {
            "sql": sql,
            "parametros": [produto.nome, produto.categoria, produto.preco],
        },
    }


@app.put("/produtos/{produto.id}")
def atualizar_produto(produto: ProdutoEntrada, produto_id: int = Path(gt=0)):

    sql_select = "SELECT id FROM produtos WHERE id = %s"
    parametros_select = (produto_id,)
    existentes = executar_sql(sql_select, parametros_select, escrita=False)

    if not existentes:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")

    sql_update = """
        UPDATE produtos
        SET nome = %s, categoria = %s, preco = %s
        WHERE id = %s
    """.strip()

    parametros_update = (produto.nome, produto.categoria, produto.preco, produto_id)

    executar_sql(sql_update, parametros_update, escrita=True)
    atualizados = executar_sql(sql_select, parametros_select, escrita=False)
    if not atualizados:
        raise HTTPException(
            status_code=404, detail="Produto não encontrado após atualização."
        )

    return {
        "dados": {
            "id": produto_id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": format(produto.preco, ".2f"),
        },
        "sintaxesql": {
            "sql": sql_update,
            "parametros": [produto.nome, produto.categoria, produto.preco, produto_id],
        },
    }
