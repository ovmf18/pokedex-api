"""Funções de acesso à PokéAPI (https://pokeapi.co/)."""

import requests

from app.models import Personagem

BASE_URL = "https://pokeapi.co/api/v2"


class PersonagemNaoEncontrado(Exception):
    """Lançada quando a PokéAPI não conhece o personagem pedido."""

    def __init__(self, nome: str):
        self.nome = nome
        super().__init__(f"Personagem '{nome}' não encontrado na PokéAPI")


class RespostaInvalidaDaPokeAPI(Exception):
    """Lançada quando a PokéAPI responde 200, mas com um corpo que não é
    JSON ou que não tem o formato esperado de um Pokémon."""


def montar_personagem(dados_json: dict) -> Personagem:
    """Converte o JSON retornado pela PokéAPI em um Personagem.

    Args:
        dados_json: resposta de GET /pokemon/{nome} já convertida em dict.

    Returns:
        Um Personagem com nome, altura, peso e tipos.
    """
    tipos_ordenados = sorted(dados_json["types"], key=lambda t: t["slot"])

    # int() garante números: se a API mandar null ou texto, a conversão
    # falha aqui em vez de gerar um Personagem inválido.
    return Personagem(
        nome=dados_json["name"],
        altura=int(dados_json["height"]),
        peso=int(dados_json["weight"]),
        tipos=[t["type"]["name"] for t in tipos_ordenados],
    )


def buscar_personagem(nome: str) -> Personagem:
    """Busca um personagem (Pokémon) na PokéAPI pelo nome.

    Args:
        nome: nome do Pokémon (ex.: "pikachu"). Não diferencia maiúsculas
            de minúsculas.

    Returns:
        O Personagem encontrado.

    Raises:
        PersonagemNaoEncontrado: se a PokéAPI responder 404.
        RespostaInvalidaDaPokeAPI: se a resposta não for JSON ou não
            tiver o formato esperado.
        requests.HTTPError: se a PokéAPI responder com outro erro.
        requests.RequestException: se a requisição falhar (conexão,
            timeout, redirecionamentos etc.).
    """
    url = f"{BASE_URL}/pokemon/{nome.lower()}"
    resposta = requests.get(url, timeout=10)
    if resposta.status_code == 404:
        raise PersonagemNaoEncontrado(nome)
    resposta.raise_for_status()

    try:
        # JSON inválido gera ValueError; campos ausentes ou com tipo
        # errado geram KeyError ou TypeError.
        return montar_personagem(resposta.json())
    except (ValueError, KeyError, TypeError) as erro:
        raise RespostaInvalidaDaPokeAPI(
            f"Resposta inesperada da PokéAPI para '{nome}': {erro!r}"
        ) from erro
