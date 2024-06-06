from pickle import dumps, loads
from time import time
from typing import Annotated

from emcache import Client
from fastapi import Depends, FastAPI, Query
from httpx import AsyncClient
from toolz import keyfilter

from insight_python.connection import getAsyncClient, getCacheClient
from insight_python.constants import DAY_IN_SECONDS
from insight_python.schemes import (
    AlfabetizationRateScheme,
    CityScheme,
    PIBScheme,
    PopulationScheme,
)

app = FastAPI()


@app.get("/cidades")
async def get_cities(
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[CityScheme]:
    URL = "/v1/localidades/estados/ce/municipios"

    if cities := await cache.get(b"cities"):
        return loads(cities.value)

    print(cities)

    res = await client.get(URL)
    cities = [keyfilter(lambda key: key in ("id", "nome"), d) for d in res.json()]

    await cache.set(
        b"cities",
        dumps(cities),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return cities


@app.get("/populacao/periodos")
async def get_population_periods(
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[int]:

    URL = "/v3/agregados/6579/periodos"

    if periods := await cache.get(b"population/periods"):
        return loads(periods.value)

    res = await client.get(URL)
    periods = [int(period["id"]) for period in res.json()]

    await cache.set(
        b"population/periods",
        dumps(periods),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return periods


@app.get("/populacao/{cityId}")
async def get_population(
    cityId: int,
    periods: Annotated[list[int] | None, Query()] = None,
    client: AsyncClient = Depends(getAsyncClient),
) -> list[PopulationScheme]:

    URL = "/v3/agregados/6579/periodos/{}/variaveis/9324".format(
        ",".join(map(str, periods)) if periods else "all"
    )

    res = await client.get(URL, params={"localidades": f"N6[{cityId}]"})
    year_and_pop: dict[str, str] = res.json()[0]["resultados"][0]["series"][0]["serie"]
    return [{"year": year, "population": pop} for year, pop in year_and_pop.items()]


@app.get("/pib/periodos")
async def get_pib_periods(
    client=Depends(getAsyncClient), cache: Client = Depends(getCacheClient)
) -> list[int]:
    URL = "/v3/agregados/5938/periodos"

    if periods := await cache.get(b"pib/periods"):
        return loads(periods.value)

    res = await client.get(URL)
    periods = [int(period["id"]) for period in res.json()]

    await cache.set(
        b"pib/periods",
        dumps(periods),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return periods


@app.get("/pib/{cityId}")
async def get_pib(
    cityId: int,
    periods: Annotated[list[int] | None, Query()] = None,
    client: AsyncClient = Depends(getAsyncClient),
) -> list[PIBScheme]:

    URL = "/v3/agregados/5938/periodos/{}/variaveis/37".format(
        ",".join(map(str, periods)) if periods else "all"
    )
    res = await client.get(URL, params={"localidades": f"N6[{cityId}]"})
    year_and_value = res.json()[0]["resultados"][0]["series"][0]["serie"]
    return [{"year": year, "value": value} for year, value in year_and_value.items()]


@app.get("/alfabetizacao/periodos")
async def get_alfabetization_periods(client=Depends(getAsyncClient)) -> list[int]:
    URL = "/v3/agregados/9543/periodos"
    res = await client.get(URL)
    return [period["id"] for period in res.json()]


@app.get("/alfabetizacao/{cityId}")
async def get_alfabetization(
    cityId: int,
    periods: Annotated[list[int] | None, Query()] = None,
    client: AsyncClient = Depends(getAsyncClient),
) -> list[AlfabetizationRateScheme]:

    URL = "/v3/agregados/9543/periodos/{}/variaveis/2513".format(
        ",".join(map(str, periods)) if periods else "all"
    )
    res = await client.get(URL, params={"localidades": f"N6[{cityId}]"})
    year_and_rate: dict[str, str] = res.json()[0]["resultados"][0]["series"][0]["serie"]
    return [{"year": year, "rate": rate} for year, rate in year_and_rate.items()]
