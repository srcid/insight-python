from pickle import dumps, loads
from time import time

from emcache import Client
from httpx import AsyncClient

from insight_python.constants import DAY_IN_SECONDS


async def get_period(aggregated: int, cache: Client, client: AsyncClient) -> list[int]:
    URL = f"/v3/agregados/{aggregated}/periodos"
    KEY = bytes(f"{aggregated}", encoding="ascii")

    if periods := await cache.get(KEY):
        return loads(periods.value)

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
) -> list[str, str]:
    URL = f"/v3/agregados/{aggregated}/periodos/{period}/variaveis/{variable}"
    KEY = bytes(f"{cityId}/{aggregated}/{period}", encoding="ascii")

    if data := await cache.get(KEY):
        return loads(data.value)

    res = await client.get(URL, params={"localidades": f"N6[{cityId}]"})
    data, *_ = res.json()[0]["resultados"][0]["series"][0]["serie"].items()

    await cache.set(
        KEY,
        dumps(data),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return data
