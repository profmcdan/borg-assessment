import uvicorn
from fastapi import FastAPI
from app import settings
from app.routers.v1.endpoints import api_router

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.include_router(api_router, prefix=settings.api_v1_prefix)

if __name__ == '__main__':
    uvicorn.run("app.main:app", port=8080, host="0.0.0.0", reload=True)
