from fastapi import FastAPI

app = FastAPI()

textos = {}

@app.hget("/posts")
async def Mostrar_posts():
    return textos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)