from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_buscar_pikachu_retorna_200_com_nome():
    resposta = client.get("/personagens/pikachu")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "pikachu"


def test_buscar_personagem_inexistente_retorna_404():
    resposta = client.get("/personagens/personagem-inexistente")

    assert resposta.status_code == 404
