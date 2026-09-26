import logging
from typing import Annotated

import requests
from fastapi import FastAPI, HTTPException, Path
from pydantic import StringConstraints

from app.models import Personagem
from app.pokeapi import (
    PersonagemNaoEncontrado,
    RespostaInvalidaDaPokeAPI,
    buscar_personagem,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="pokedex-api")

# Espaços nas pontas são removidos antes de validar; depois disso, só
# letras, números e hífen (ex.: "mr-mime", "25"). Isso impede que o
# nome altere a URL enviada à PokéAPI (".", "..", "?", "#", "/").
NomePokemon = Annotated[
    str,
    StringConstraints(strip_whitespace=True),
    Path(
        pattern=r"^[A-Za-z0-9-]+$",
        max_length=50,
        description="Nome ou número do Pokémon na Pokédex. "
        "Aceita letras, números e hífen.",
        examples=["pikachu", "mr-mime", "25"],
    ),
]


@app.get("/")
def raiz() -> dict:
    return {"mensagem": "Hello, treinador!"}


# Função síncrona (def, não async def) porque buscar_personagem usa
# requests, que bloqueia; o FastAPI a executa em uma thread separada.
@app.get(
    "/personagens/{nome}",
    responses={
        404: {"description": "Personagem não encontrado"},
        422: {"description": "Nome inválido (use apenas letras, números e hífen)"},
        502: {"description": "A PokéAPI respondeu com erro ou com dados inválidos"},
        503: {"description": "PokéAPI indisponível ou limitando requisições"},
    },
)
def obter_personagem(nome: NomePokemon) -> Personagem:
    try:
        return buscar_personagem(nome)
    except PersonagemNaoEncontrado:
        raise HTTPException(
            404,
            f"Não encontramos nenhum Pokémon chamado '{nome}'. "
            "Confira se o nome está escrito corretamente.",
        )
    except RespostaInvalidaDaPokeAPI:
        logger.exception("Resposta inválida da PokéAPI ao buscar %r", nome)
        raise HTTPException(502, "A PokéAPI respondeu com dados inválidos.")
    except (requests.ConnectionError, requests.Timeout) as erro:
        logger.warning("PokéAPI indisponível ao buscar %r: %r", nome, erro)
        raise HTTPException(
            503,
            "A PokéAPI está indisponível no momento. Tente novamente em instantes.",
        )
    except requests.HTTPError as erro:
        status = erro.response.status_code if erro.response is not None else None
        if status == 429:
            logger.warning("PokéAPI limitou as requisições ao buscar %r", nome)
            retry_after = erro.response.headers.get("Retry-After")
            raise HTTPException(
                503,
                "A PokéAPI está recebendo muitas requisições. "
                "Tente novamente em instantes.",
                headers={"Retry-After": retry_after} if retry_after else None,
            )
        logger.warning("PokéAPI respondeu %s ao buscar %r", status, nome)
        raise HTTPException(502, "A PokéAPI respondeu com um erro inesperado.")
    except requests.RequestException:
        # Demais falhas do requests: conexão interrompida no meio da
        # resposta, redirecionamentos em excesso etc.
        logger.exception("Falha inesperada ao consultar a PokéAPI para %r", nome)
        raise HTTPException(502, "Não foi possível obter os dados da PokéAPI.")
