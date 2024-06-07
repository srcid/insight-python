import emcache
from httpx import AsyncClient


async def getAsyncClient():
    async with AsyncClient(
        base_url="https://servicodados.ibge.gov.br/api", timeout=5
    ) as client:
        yield client


async def getCacheClient():
    client = await emcache.create_client(
        [emcache.MemcachedHostAddress("memcached", 11211)]
    )
    yield client
    await client.close()
