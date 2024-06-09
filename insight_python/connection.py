import emcache
from httpx import AsyncClient

from insight_python.settings import settings


async def getAsyncClient():
    async with AsyncClient(
        base_url="https://servicodados.ibge.gov.br/api", timeout=10
    ) as client:
        yield client


async def getCacheClient():
    client = await emcache.create_client(
        [emcache.MemcachedHostAddress(settings.MEMCACHED_URL, 11211)]
    )
    yield client
    await client.close()
