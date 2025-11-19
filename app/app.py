from fastapi import FastAPI, HTTPException,File, UploadFile,Form,Depends
from app.biblioteca import textos
from app.schemas import TypeDataPost,TypeDataReturn
from app.db import Post, get_session, criar_db_e_tabelas
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
import uuid
from app.imagens import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import os
import shutil
import tempfile 




@asynccontextmanager
async def lifespan(app: FastAPI):
    await criar_db_e_tabelas()
    yield

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}

@app.post("/upload")
async def upload_arquivo(
    arquivo: UploadFile = File(...),
    legenda: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(arquivo.filename)[1]) as arquivo_temporario:
            path_arquivo_temporario = arquivo_temporario.name
            shutil.copyfileobj(arquivo.file, arquivo_temporario)

            upload_resultado = imagekit.upload_file(
                file=open(path_arquivo_temporario, "rb"),
                file_name=arquivo.filename,
                options=UploadFileRequestOptions(
                    use_unique_file_name=True,
                    tags = ["backend-upload"]
                )
            )

            if upload_resultado.response_metadata.http_status_code == 200:
                post = Post(
                        legenda = legenda,
                        url = upload_resultado.url,
                        tipo_arquivo = "video" if arquivo.content_type.startswith("video/") else "imagem",
                        nome_arquivo = upload_resultado.name
                )
                session.add(post)
                await session.commit()
                await session.refresh(post)
                return post 

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload do arquivo: {e}")
    finally:
        if path_arquivo_temporario and os.path.exists(path_arquivo_temporario):
            os.unlink(path_arquivo_temporario) 
        arquivo.file.close()


    


@app.get("/feed")
async def obter_feed(
    session: AsyncSession = Depends(get_session)
):
    resultado = await session.execute(select(Post).order_by(Post.criado_em.desc()))
    posts = [linha[0] for linha in resultado.all()]
    
    posts_formatados = []

    for post in posts:
        posts_formatados.append(
            {
            "id": str(post.id),
            "legenda": post.legenda,
            "url": post.url,
            "tipo_arquivo": post.tipo_arquivo,
            "nome_arquivo": post.nome_arquivo,
            "criado_em": post.criado_em.isoformat()
        }
        )
    return {"posts": posts_formatados}

@app.delete("/post/{post_id}")
async def deletar_post(
    post_id:uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    resultado = await session.execute(select(Post).where(Post.id == post_id))
    post = resultado.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Publicação não encontrada")
    await session.delete(post)
    await session.commit()
    return {"message": "Post deleted successfully"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

    
