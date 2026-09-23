"""Funções de acesso à PokéAPI (https://pokeapi.co/)."""

import requests

from app.models import Personagem

BASE_URL = "https://pokeapi.co/api/v2"


def montar_personagem(dados_json: dict) -> Personagem:
    """Converte o JSON retornado pela PokéAPI em um Personagem.

    Args:
        dados_json: resposta de GET /pokemon/{nome} já convertida em dict.

    Returns:
        Um Personagem com nome, altura, peso e tipos.
    """
    tipos_ordenados = sorted(dados_json["types"], key=lambda t: t["slot"])

    return Personagem(
        nome=dados_json["name"],
        altura=dados_json["height"],
        peso=dados_json["weight"],
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
        requests.HTTPError: se o Pokémon não for encontrado ou a
            requisição falhar.
    """
    url = f"{BASE_URL}/pokemon/{nome.lower()}"
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()

    return montar_personagem(resposta.json())
