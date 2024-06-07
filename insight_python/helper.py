from pickle import dumps, loads
from time import time

from emcache import Client
from httpx import AsyncClient

from insight_python.constants import DAY_IN_SECONDS


async def get_period(aggregated: int, cache: Client, client: AsyncClient) -> list[int]:
    URL = f"/v3/agregados/{aggregated}/periodos"

    if periods := await cache.get(bytes(f"{aggregated}/periods", encoding="ascii")):
        return loads(periods.value)

    res = await client.get(URL)
    periods = [int(period["id"]) for period in res.json()]

    await cache.set(
        bytes(f"{aggregated}/periods", encoding="ascii"),
        dumps(periods),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return periods
