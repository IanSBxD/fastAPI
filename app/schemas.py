from pydantic import BaseModel

class TypeDataPost(BaseModel):
    titulo: str
    conteudo: str

class TypeDataReturn(BaseModel):
    titulo: str
    conteudo: str