from pydantic import BaseModel

class TypeDataPost(BaseModel):
    titulo: str
    conteudo: str