import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_get_test():
  async with AsyncClient(app=app, base_url='http://test') as ac:
    response = await ac.get('/test')
  assert response.status_code == 200

# @pytest.mark.asyncio
# async def test_get_msg():
  # async with AsyncClient(app=app, base_url='http://test') as ac:
    # response = await ac.get('/message/1')
  # assert response.status_code == 200