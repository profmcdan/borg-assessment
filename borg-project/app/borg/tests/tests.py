import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.borg.models import Url


@pytest.mark.asyncio
async def test_create_url(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    payload = test_data["case_create"]["payload"]
    response = await async_client.post(
        "/api/v1/urls",
        json=payload,
    )

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_create"]["want"]

    for k, v in want.items():
        assert got[k] == v

    statement = select(Url).where(Url.id == got["id"])
    results = await async_session.execute(statement=statement)
    hero = results.scalar_one()

    for k, v in want.items():
        assert getattr(hero, k) == v


@pytest.mark.asyncio
async def test_get_url(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    url_data = test_data["initial_data"]["hero"]
    statement = insert(Url).values(url_data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.get(f"/api/v1/urls/{url_data['id']}")
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_get"]["want"]

    for k, v in want.items():
        assert got[k] == v


@pytest.mark.asyncio
async def test_patch_url(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    data = test_data["initial_data"]["url"]
    statement = insert(Url).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    payload = test_data["case_patch"]["payload"]
    response = await async_client.patch(f"/api/v1/urls/{data['id']}", json=payload)
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_patch"]["want"]

    for k, v in want.items():
        assert got[k] == v


@pytest.mark.asyncio
async def test_delete_hero(
    async_client: AsyncClient, async_session: AsyncSession, test_data: dict
):
    data = test_data["initial_data"]["url"]
    statement = insert(Url).values(data)
    await async_session.execute(statement=statement)
    await async_session.commit()

    response = await async_client.delete(f"/api/v1/urls/{data['id']}")
    assert response.status_code == 200

    got = response.json()
    want = test_data["case_delete"]["want"]

    for k, v in want.items():
        assert got[k] == v

    statement = select(Url).where(Url.id == data["id"])
    results = await async_session.execute(statement=statement)
    url = results.scalar_one_or_none()

    assert url is None
