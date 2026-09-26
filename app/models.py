"""Modelos de dados do projeto."""

from dataclasses import dataclass

# Nomes oficiais dos tipos nos jogos em português.
TIPOS_EM_PORTUGUES = {
    "normal": "normal",
    "fighting": "lutador",
    "flying": "voador",
    "poison": "venenoso",
    "ground": "terrestre",
    "rock": "pedra",
    "bug": "inseto",
    "ghost": "fantasma",
    "steel": "aço",
    "fire": "fogo",
    "water": "água",
    "grass": "planta",
    "electric": "elétrico",
    "psychic": "psíquico",
    "ice": "gelo",
    "dragon": "dragão",
    "dark": "sombrio",
    "fairy": "fada",
}


@dataclass
class Personagem:
    """Um personagem (Pokémon).

    Attributes:
        nome: nome do Pokémon.
        altura: altura em decímetros, como a PokéAPI retorna.
        peso: peso em hectogramas, como a PokéAPI retorna.
        tipos: nomes dos tipos, na ordem dos slots (ex.: ["grass", "poison"]).
    """

    nome: str
    altura: int
    peso: int
    tipos: list[str]

    def resumo(self) -> str:
        """Descreve o personagem em uma frase.

        Ex.: "Pikachu é do tipo elétrico, pesa 6kg e mede 40cm".
        """
        tipos = [TIPOS_EM_PORTUGUES.get(t, t) for t in self.tipos]
        if len(tipos) > 1:
            texto_tipos = ", ".join(tipos[:-1]) + " e " + tipos[-1]
        elif tipos:
            texto_tipos = tipos[0]
        else:
            texto_tipos = "desconhecido"

        # 1 hg = 0,1 kg; o formato "g" omite o ",0" de pesos inteiros.
        peso_kg = f"{self.peso / 10:g}".replace(".", ",")
        # 1 dm = 10 cm.
        altura_cm = self.altura * 10

        return (
            f"{self.nome.capitalize()} é do tipo {texto_tipos}, "
            f"pesa {peso_kg}kg e mede {altura_cm}cm"
        )
