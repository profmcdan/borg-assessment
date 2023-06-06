import pickle
import uuid
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi import status as http_status
from typing import List

from urllib.parse import unquote
from app.core.models import StatusMessage
from app.core.redis import cache
from .repository import UrlRepository
from .dependencies import get_bityl_repository
from .schemas import UrlCreate, UrlPatch, UrlRead, UrlBase
from .services import generate_short_url, clean_url

router = APIRouter()


@router.get("", response_model=List[UrlRead], status_code=http_status.HTTP_200_OK)
async def get_urls(
    limit: int = Query(default=10, lte=50),
    offset: int = Query(default=0),
    repo: UrlRepository = Depends(get_bityl_repository),
):
    urls = await repo.get_all()
    return urls


@router.post("", response_model=UrlRead, status_code=http_status.HTTP_201_CREATED)
async def create_url(
    data: UrlCreate, repo: UrlRepository = Depends(get_bityl_repository)
):
    found = await repo.get_by_original_url(clean_url(data.original_url))
    if found is not None:
        raise HTTPException(
            status_code=http_status.HTTP_409_CONFLICT, detail="Url already exists"
        )

    generated_url = generate_short_url(data.original_url)
    new_url: dict = {
        "original_url": clean_url(data.original_url),
        "short_url": generated_url["short_url"],
        "code": generated_url["code"],
        "expiry_date": datetime.now() + timedelta(days=30),
        "owner_id": str(uuid.uuid4()),
    }

    url = await repo.create(data=UrlBase(**new_url))
    return url


@router.get("/{id}", response_model=UrlRead, status_code=http_status.HTTP_200_OK)
async def get_url_by_id(
    id: str, repo: UrlRepository = Depends(get_bityl_repository), redis=Depends(cache)
):
    url = await repo.get(id=id)
    if url is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Url not found"
        )

    redis.set(f"url_{url.short_url}", pickle.dumps(url))
    return url


@router.get("/code/{code}", response_model=UrlRead, status_code=http_status.HTTP_200_OK)
async def get_url_by_code(
    code: str, repo: UrlRepository = Depends(get_bityl_repository), redis=Depends(cache)
):
    # code = short_url.split('/')[-1]

    if (cached_profile := redis.get(f"url_{str(code)}")) is not None:
        return pickle.loads(cached_profile)

    url = await repo.get_by_code(code=code)
    if url is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Url not found"
        )

    redis.set(f"url_{str(code)}", pickle.dumps(url))
    return url


@router.get(
    "/get-url/redirect", response_model=UrlRead, status_code=http_status.HTTP_200_OK
)
async def get_url_by_short_code(
    short_url: str = Query(..., min_length=1, max_length=50),
    repo: UrlRepository = Depends(get_bityl_repository),
    redis=Depends(cache),
):
    short_url = unquote(short_url)
    code = short_url.split("/")[-1]

    if (cached_profile := redis.get(f"url_{str(code)}")) is not None:
        return pickle.loads(cached_profile)

    url = await repo.get_by_short_url(short_url=short_url)
    if url is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Url not found"
        )

    redis.set(f"url_{str(code)}", pickle.dumps(url))
    return url


@router.patch("/{id}", response_model=UrlRead, status_code=http_status.HTTP_200_OK)
async def update_url(
    id: str,
    data: UrlPatch,
    repo: UrlRepository = Depends(get_bityl_repository),
    redis=Depends(cache),
):
    url = await repo.get(id=id)
    if url is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Url not found"
        )

    updated_url = await repo.patch(id=id, data=data)
    redis.delete(f"profile_{updated_url.code}")
    return url


@router.delete(
    "/{id}", response_model=StatusMessage, status_code=http_status.HTTP_200_OK
)
async def delete_url(
    id: str, repo: UrlRepository = Depends(get_bityl_repository), redis=Depends(cache)
):
    url = await repo.get(id=id)
    if url is None:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND, detail="Url not found"
        )

    status = await repo.delete(id=id)
    redis.delete(f"profile_{url.code}")
    return {"status": status, "message": "The url has been deleted!"}
