from pickle import dumps, loads
from time import time
from typing import Any

from emcache import Client
from httpx import AsyncClient

from insight_python.constants import DAY_IN_SECONDS


async def get_period(aggregated: int, cache: Client, client: AsyncClient) -> list[int]:
    URL = f"/v3/agregados/{aggregated}/periodos"
    KEY = bytes(f"{aggregated}", encoding="ascii")

    if periods_cache := await cache.get(KEY):
        return loads(periods_cache.value)

    res = await client.get(URL)
    periods = [int(period["id"]) for period in res.json()]

    await cache.set(
        KEY,
        dumps(periods),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return periods


async def get_data(
    aggregated: int,
    period: int,
    variable: int,
    cityId: int,
    client: AsyncClient,
    cache: Client,
) -> Any:
    URL = f"/v3/agregados/{aggregated}/periodos/{period}/variaveis/{variable}"
    KEY = bytes(f"{cityId}/{aggregated}/{period}", encoding="ascii")

    if data_cache := await cache.get(KEY):
        return loads(data_cache.value)

    res = await client.get(URL, params={"localidades": f"N6[{cityId}]"})
    data = res.json()[0]["resultados"][0]["series"][0]["serie"][f"{period}"]

    await cache.set(
        KEY,
        dumps(data),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return data
