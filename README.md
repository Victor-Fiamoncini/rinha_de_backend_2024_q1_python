# Rinha de Backend Python - 2024 Q1

Minha versão em Python com o framework Flask para a rinha de backend. Feita usando clean-arch e conceitos de DDD (apenas para testar como se sai em relação a performance).

Desafio para a Rinha de Backend - 2024 Q1 (Feita semanas depois da competição ter acabado).

Principais ferramentas usadas:

- Python v3.11.6;
- Flask v3.0.1;
- Postgres v15.

## Como iniciar (build desenvolvimento) 🛠

```bash
cp .env.example .env # Cria um novo arquivo de environment

docker-compose -f docker-compose-dev.yml up --build # Inicia os containers (Postgres e Python) e executa o servidor Flask em modo debug
```

## Como iniciar (executar testes unitários/integração) 🛠

```bash
cp .env.example .env # Cria um novo arquivo de environment

docker-compose -f docker-compose-dev.yml up --build # Inicia os containers (Postgres e Python) e executa o servidor Flask em modo debug

docker exec -it app_dev bash # Inicia o terminal (usando bash) dentro do container Python

sh run_integration_tests.sh # Executa os testes de integração (após cada teste o Postgres é dropado e iniciado novamente)

sh run_unit_tests.sh # Executa os testes unitários
```

----------
Released in 2024

By [Victor B. Fiamoncini](https://github.com/Victor-Fiamoncini) ☕️

