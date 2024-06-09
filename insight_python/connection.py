import emcache
from httpx import AsyncClient

from insight_python.settings import settings


async def getAsyncClient():
    async with AsyncClient(
        base_url="https://servicodados.ibge.gov.br/api", timeout=10
    ) as client:
        yield client


async def getCacheClient():
    servers = []
    for uri in settings.MEMCACHED_SERVERS.split(","):
        url, port = uri.split(":")
        port = int(port)
        servers.append(emcache.MemcachedHostAddress(url, port))

    client = await emcache.create_client(servers, timeout=20)
    yield client
    await client.close()
