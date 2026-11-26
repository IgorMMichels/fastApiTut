import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

def executar_sql(sql, parametros=(), escrita=False):
    conexao = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(sql, parametros)

        if escrita:
            conexao.commit()
            resultado = {
                'id_gerado': cursor.lastrowid,
                'linhas_afetadas': cursor.rowcount,
            }
            return resultado
        else:
            return cursor.fetchall()

    except Exception:
        conexao.rollback()
        raise
       
    finally:
        if cursor is not None:
            cursor.close()
        conexao.close()    
