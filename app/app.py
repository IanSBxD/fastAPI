from fastapi import FastAPI, HTTPException
from app.biblioteca import textos
from app.schemas import TypeDataPost

app = FastAPI()

@app.get("/posts")
async def Mostrar_posts(limite:int = None):
    if limite:
        return list(textos.values())[:limite]
    return textos

@app.get("/posts/{id_post}")
async def mostrar_post_especifico(id_post:int):
    if id_post not in textos:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    return textos.get(id_post, {"erro": "Post não encontrado"})

@app.post("/posts")
async def criar_post(id:int, post: TypeDataPost):
    if id in textos:
        raise HTTPException(status_code=400, detail="Post com esse ID já existe")
    
    max_id = max(textos.keys()) if textos else 0
    if id > max_id + 1:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    textos[id] = {
        "titulo": post.titulo,
        "conteudo": post.conteudo
    }
    return textos[id]

@app.delete("/posts/{id_post}")
async def deletar_post(id_post:int):
    if id_post not in textos:
        raise HTTPException(status_code=404, detail="post nao encontrado")
    del textos[id_post]
    return {"detail": "Post deletado com sucesso"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)