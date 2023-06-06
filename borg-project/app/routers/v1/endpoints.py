from fastapi import APIRouter

from app.borg.routes import router as url_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (url_router, "urls", "urls"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")


