# pokedex-api

Este projeto será uma API de personagens de jogos da franquia Pokémon.

## Como executar

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API fica disponível em http://127.0.0.1:8000 e a documentação interativa em http://127.0.0.1:8000/docs.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/personagens/{nome}` | Nome, altura, peso e tipos do Pokémon (404 se não existir) |

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes consultam a PokéAPI de verdade, então precisam de internet.
