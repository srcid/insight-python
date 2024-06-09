from asyncio import gather
from pickle import dumps, loads
from time import time
from typing import Annotated

from emcache import Client
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from toolz import keyfilter

from insight_python.connection import getAsyncClient, getCacheClient
from insight_python.constants import (
    AGGREGATED_GDP,
    AGGREGATED_LITERACY,
    AGGREGATED_POPULATION,
    DAY_IN_SECONDS,
    VARIABLE_GDP_CURRENT_PRICES,
    VARIABLE_LITERACY_15_PLUS_PEOPLE,
    VARIABLE_POPULATION_ESTIMATED_RESIDENT,
)
from insight_python.helper import get_data, get_period
from insight_python.schemes import (
    CityScheme,
    GDPScheme,
    LiteracyRateScheme,
    PopulationScheme,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/cidades")
async def get_cities(
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[CityScheme]:
    URL = "/v1/localidades/estados/ce/municipios"

    if res_cache := await cache.get(b"cities"):
        return loads(res_cache.value)

    res = await client.get(URL)
    cities = [keyfilter(lambda key: key in ("id", "nome"), d) for d in res.json()]

    await cache.set(
        b"cities",
        dumps(cities),
        exptime=int(time()) + DAY_IN_SECONDS,
        noreply=True,
    )

    return [CityScheme(**city) for city in cities]


@app.get("/populacao/periodos")
async def get_population_periods(
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[int]:

    return await get_period(AGGREGATED_POPULATION, cache, client)


@app.get("/populacao/{cityId}")
async def get_population(
    cityId: int,
    periods: Annotated[list[int] | None, Query(alias="periodos")] = None,
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[PopulationScheme]:

    if not periods:
        periods = await get_period(AGGREGATED_POPULATION, cache, client)

    data = await gather(
        *[
            get_data(
                AGGREGATED_POPULATION,
                period,
                VARIABLE_POPULATION_ESTIMATED_RESIDENT,
                cityId,
                client,
                cache,
            )
            for period in periods
        ]
    )

    return [
        PopulationScheme(year=year, population=population) for year, population in data
    ]


@app.get("/pib/periodos")
async def get_pib_periods(
    client=Depends(getAsyncClient), cache: Client = Depends(getCacheClient)
) -> list[int]:

    return await get_period(AGGREGATED_GDP, cache, client)


@app.get("/pib/{cityId}")
async def get_pib(
    cityId: int,
    periods: Annotated[list[int] | None, Query(alias="periodos")] = None,
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[GDPScheme]:

    if not periods:
        periods = await get_period(AGGREGATED_GDP, cache, client)

    data = await gather(
        *[
            get_data(
                AGGREGATED_GDP,
                period,
                VARIABLE_GDP_CURRENT_PRICES,
                cityId,
                client,
                cache,
            )
            for period in periods
        ]
    )

    return [GDPScheme(year=year, value=value) for year, value in data]


@app.get("/alfabetizacao/periodos")
async def get_alfabetization_periods(
    client=Depends(getAsyncClient), cache: Client = Depends(getCacheClient)
) -> list[int]:

    return await get_period(AGGREGATED_LITERACY, cache, client)


@app.get("/alfabetizacao/{cityId}")
async def get_alfabetization(
    cityId: int,
    periods: Annotated[list[int] | None, Query(alias="periodos")] = None,
    client: AsyncClient = Depends(getAsyncClient),
    cache: Client = Depends(getCacheClient),
) -> list[LiteracyRateScheme]:

    if not periods:
        periods = await get_period(AGGREGATED_LITERACY, cache, client)

    data = await gather(
        *[
            get_data(
                AGGREGATED_LITERACY,
                period,
                VARIABLE_LITERACY_15_PLUS_PEOPLE,
                cityId,
                client,
                cache,
            )
            for period in periods
        ]
    )

    return [LiteracyRateScheme(year=year, rate=rate) for year, rate in data]
