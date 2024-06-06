from pydantic import BaseModel, ConfigDict, Field


class CommonConfigs(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class CityScheme(CommonConfigs):
    id: int
    name: str = Field(alias="nome")


class PopulationScheme(CommonConfigs):
    year: int = Field(alias="ano")
    population: int = Field(alias="population")


class PIBScheme(CommonConfigs):
    year: int = Field(alias="ano")
    value: int = Field(alias="valor")


class AlfabetizationRateScheme(CommonConfigs):
    year: int = Field(alias="ano")
    rate: float = Field(alias="taxa")
