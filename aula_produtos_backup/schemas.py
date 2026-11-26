from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class ProdutoEntrada(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    
    nome: str = Field(min_length=1, max_length=100)
    categoria: str = Field(min_length=1, max_length=50)
    preco: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    