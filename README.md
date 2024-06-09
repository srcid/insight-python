# INSIGHT-PYTHON

FastAPI backend sample for InsightLab job position.

## Front-end

O front-end desse projeto encontra-se no seguinte repósitorio srcid/rAPIdinho.

## IBGE endpoints used

Endpoints used on this project.

### Cidades do Ceará
https://servicodados.ibge.gov.br/api/v1/localidades/estados/ce/municipios

### População
https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/2021/variaveis/9324

### PIB
https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2021/variaveis/37

### Alfabetização
https://servicodados.ibge.gov.br/api/v3/agregados/9543/periodos/2022/variaveis/2513


## How to run

To run this project, you will need to have Docker installed on your system.

### Run the compose

Run the command bellow, you can also use the `-d` to hide the logs. Depending of the 
version of your docker compose, you may need to use `docker-compose` instead.

```shell
docker compose up
```

### Stop the compose

Run the command bellow. Use the flag `--rmi all` to remove the downloaded images from
your system.

```shell
docker compose down
```