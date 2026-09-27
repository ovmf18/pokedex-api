# Pokédex API

API REST em Python com [FastAPI](https://fastapi.tiangolo.com/) que consome a [PokéAPI](https://pokeapi.co/) e devolve os dados de um Pokémon (nome, altura, peso e tipos) em um JSON simples.

```http
GET /personagens/pikachu
```

```json
{
  "nome": "pikachu",
  "altura": 4,
  "peso": 60,
  "tipos": ["electric"]
}
```

## Destaques

- **Validação de entrada:** o nome aceita só letras, números e hífen (até 50 caracteres), e espaços nas pontas são removidos. Entradas como `..`, `?` ou `#` são recusadas antes de chegar à PokéAPI.
- **Tratamento de erros da API externa:** cada falha vira um código HTTP com mensagem clara, e a causa fica registrada no log.
- **Documentação automática:** a tela `/docs` (Swagger UI) mostra o que a API espera receber e devolver, inclusive os códigos de erro.
- **Testes automatizados** com pytest e o `TestClient` do FastAPI.

## Tecnologias

Python · FastAPI · Uvicorn · Requests · Pytest

## Como executar

Requer Python 3.12 (versão usada no desenvolvimento).

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API fica em http://127.0.0.1:8000 e a documentação interativa em http://127.0.0.1:8000/docs.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/personagens/{nome}` | Dados do Pokémon pelo nome ou número da Pokédex (ex.: `pikachu`, `mr-mime`, `25`) |

A altura vem em **decímetros** e o peso em **hectogramas**, como na PokéAPI (`altura: 4` = 40 cm, `peso: 60` = 6 kg).

### Respostas de erro

| Código | Quando acontece |
|---|---|
| 404 | O Pokémon não existe |
| 422 | O nome tem caracteres inválidos |
| 502 | A PokéAPI respondeu com erro ou com dados inválidos |
| 503 | A PokéAPI está fora do ar, demorou demais ou está limitando requisições |

Exemplo de 404:

```json
{
  "detail": "Não encontramos nenhum Pokémon chamado 'naoexiste'. Confira se o nome está escrito corretamente."
}
```

## Testes

```bash
pip install -r requirements-dev.txt
pytest
```

Os testes consultam a PokéAPI de verdade, então precisam de internet.

## Estrutura

```
app/
├── main.py      # aplicação FastAPI, rotas e tratamento de erros
├── pokeapi.py   # cliente da PokéAPI e conversão do JSON
└── models.py    # dataclass Personagem
tests/
└── test_personagens.py
```

## Créditos

Dados fornecidos pela [PokéAPI](https://pokeapi.co/). Pokémon e seus nomes são marcas registradas da Nintendo, Game Freak e The Pokémon Company. Este é um projeto de estudo, sem fins comerciais.
