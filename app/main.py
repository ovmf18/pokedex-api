import requests
from fastapi import FastAPI, HTTPException

from app.models import Personagem
from app.pokeapi import buscar_personagem

app = FastAPI(title="pokedex-api")


@app.get("/")
def raiz() -> dict:
    return {"mensagem": "Hello, treinador!"}


# Função síncrona (def, não async def) porque buscar_personagem usa
# requests, que bloqueia; o FastAPI a executa em uma thread separada.
@app.get("/personagens/{nome}")
def obter_personagem(nome: str) -> Personagem:
    try:
        return buscar_personagem(nome)
    except requests.HTTPError as erro:
        if erro.response is not None and erro.response.status_code == 404:
            raise HTTPException(404, f"Personagem '{nome}' não encontrado")
        raise HTTPException(502, "Erro ao consultar a PokéAPI")
    except requests.RequestException:
        raise HTTPException(502, "Não foi possível conectar à PokéAPI")
