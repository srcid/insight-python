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
        [
            emcache.MemcachedHostAddress(server, 11211)
            for server in settings.MEMCACHEDCLOUD_SERVERS.split(",")
        ]
    )
    yield client
    await client.close()
