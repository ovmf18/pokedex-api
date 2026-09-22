"""Funções de acesso à PokéAPI (https://pokeapi.co/)."""

import requests

BASE_URL = "https://pokeapi.co/api/v2"


def buscar_personagem(nome: str) -> dict:
    """Busca um personagem (Pokémon) na PokéAPI pelo nome.

    Args:
        nome: nome do Pokémon (ex.: "pikachu"). Não diferencia maiúsculas
            de minúsculas.

    Returns:
        Um dicionário com "nome" e "altura" do Pokémon. A altura é
        retornada em decímetros, conforme a própria PokéAPI.

    Raises:
        requests.HTTPError: se o Pokémon não for encontrado ou a
            requisição falhar.
    """
    url = f"{BASE_URL}/pokemon/{nome.lower()}"
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()

    return {
        "nome": dados["name"],
        "altura": dados["height"],
    }
