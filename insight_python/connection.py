from httpx import AsyncClient, AsyncHTTPTransport
import httpx


async def getAsyncClient():
    async with AsyncClient(
        base_url="https://servicodados.ibge.gov.br/api", timeout=5
    ) as client:
        yield client
