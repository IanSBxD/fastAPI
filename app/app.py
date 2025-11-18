from fastapi import FastAPI, HTTPException,File, UploadFile,Form,Depends
from app.biblioteca import textos
from app.schemas import TypeDataPost,TypeDataReturn
from app.db import Post, get_session, criar_db_e_tabelas
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    await criar_db_e_tabelas()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_arquivo(
    arquivo: UploadFile = File(...),
    legenda: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    post = Post(
        legenda = legenda,
        url = "qualquercoisa",
        tipo_arquivo = "foto",
        nome_arquivo = "nome_arquivo"
    )
    
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def obter_feed(
    session: AsyncSession = Depends(get_session)
):
    resultado = await session.execute(select(Post).order_by(Post.criado_em.desc()))
    posts = resultado.scalars().all()
    return posts
    
    
