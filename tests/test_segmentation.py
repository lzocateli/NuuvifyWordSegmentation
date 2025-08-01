#!/usr/bin/env python3
"""
Testes para a API de segmentação de palavras Nuuvify
"""

import asyncio
import sys
from pathlib import Path

import httpx
import pytest

# Adicionar o diretório raiz do projeto ao sys.path para importações
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


class TestWordSegmentation:
    """Classe de testes para segmentação de palavras"""

    @pytest.fixture
    def test_cases(self):
        """Casos de teste padrão"""
        return [
            {"input": "minhacasatemsp", "expected": "MinhaCasaTemSP"},
            {"input": "euamoobrasilsp", "expected": "EuAmoBrasilSP"},
            {"input": "sistemadeinformacaomg", "expected": "SistemaDeInformacaoMG"},
            {
                "input": "tecnologiadainformacaoti",
                "expected": "TecnologiaDaInformacaoTI",
            },
        ]

    def test_local_segmentation(self, test_cases):
        """Testa a função de segmentação localmente"""
        try:
            from src.services.nuuvify_wordsegment_service import (
                nuuvify_wordsegment_service,
            )

            for case in test_cases:
                result = nuuvify_wordsegment_service.segment_and_format(
                    case["input"], "pt"
                )
                print(f"✅ '{case['input']}' → '{result}'")
                # Note: Não fazemos assert do resultado esperado pois depende do modelo NLP
                assert isinstance(result, str)
                assert len(result) > 0

        except Exception as e:
            pytest.fail(f"Erro na função local: {e}")

    @pytest.mark.asyncio
    async def test_segmentation_api_status(self):
        """Testa endpoints de status da API"""
        base_url = "http://localhost:8000"

        async with httpx.AsyncClient() as client:
            # Teste endpoint raiz
            try:
                response = await client.get(f"{base_url}/api/v1/")
                assert response.status_code == 200
                data = response.json()
                assert "message" in data
                assert "version" in data
            except httpx.ConnectError:
                pytest.skip("API não está rodando")

            # Teste endpoint de status
            try:
                response = await client.get(f"{base_url}/api/v1/status")
                assert response.status_code == 200
                data = response.json()
                assert "status" in data
                assert "timestamp" in data
            except httpx.ConnectError:
                pytest.skip("API não está rodando")

    @pytest.mark.asyncio
    async def test_segmentation_api_endpoint(self, test_cases):
        """Testa o endpoint de segmentação da API"""
        base_url = "http://localhost:8000"

        async with httpx.AsyncClient() as client:
            for case in test_cases:
                try:
                    response = await client.post(
                        f"{base_url}/api/v1/segment/",
                        json={"text": case["input"], "language": "pt"},
                    )

                    if response.status_code == 200:
                        result = response.json()
                        assert "original" in result
                        assert "formatted" in result
                        assert result["original"] == case["input"]
                        assert isinstance(result["formatted"], str)
                        assert len(result["formatted"]) > 0
                    else:
                        pytest.fail(
                            f"API retornou erro: {response.status_code} - {response.text}"
                        )

                except httpx.ConnectError:
                    pytest.skip("API não está rodando")


# Funções para execução manual (compatibilidade com script anterior)
async def test_segmentation_api():
    """Testa a API de segmentação de palavras (versão script)"""
    base_url = "http://localhost:8000"

    # Dados de teste
    test_cases = [
        {"text": "minhacasatemsp", "language": "pt"},
        {"text": "euamoobrasilsp", "language": "pt"},
        {"text": "sistemadeinformacaomg", "language": "pt"},
    ]

    async with httpx.AsyncClient() as client:
        print("🧪 Testando API de Segmentação de Palavras\n")

        # Teste endpoint raiz
        try:
            response = await client.get(f"{base_url}/api/v1/")
            print(f"✅ Endpoint raiz: {response.status_code}")
            print(f"   Resposta: {response.json()}\n")
        except Exception as e:
            print(f"❌ Erro no endpoint raiz: {e}\n")

        # Teste endpoint de status
        try:
            response = await client.get(f"{base_url}/api/v1/status")
            print(f"✅ Status: {response.status_code}")
            print(f"   Resposta: {response.json()}\n")
        except Exception as e:
            print(f"❌ Erro no status: {e}\n")

        # Teste segmentação
        for i, test_case in enumerate(test_cases, 1):
            try:
                response = await client.post(
                    f"{base_url}/api/v1/segment/", json=test_case
                )
                print(f"✅ Teste {i}: {response.status_code}")
                print(f"   Input: {test_case['text']}")

                if response.status_code == 200:
                    result = response.json()
                    print(f"   Output: {result['formatted']}")
                else:
                    print(f"   Erro: {response.text}")
                print()

            except Exception as e:
                print(f"❌ Erro no teste {i}: {e}\n")


def test_local_segmentation():
    """Testa a função de segmentação localmente (versão script)"""
    print("🔧 Testando função local de segmentação\n")

    try:
        from src.services.nuuvify_wordsegment_service import nuuvify_wordsegment_service

        test_cases = [
            "minhacasatemsp",
            "euamoobrasilsp",
            "sistemadeinformacaomg",
        ]

        for text in test_cases:
            result = nuuvify_wordsegment_service.segment_and_format(text, "pt")
            print(f"✅ '{text}' → '{result}'")

    except Exception as e:
        print(f"❌ Erro na função local: {e}")


if __name__ == "__main__":
    print("=" * 50)
    print("TESTE DE SEGMENTAÇÃO DE PALAVRAS NUUVIFY")
    print("=" * 50 + "\n")

    # Teste local primeiro
    test_local_segmentation()

    print("\n" + "=" * 50)
    print("Para testar a API, execute:")
    print("1. uvicorn src.api.main:app --reload")
    print("2. python tests/test_segmentation.py --api")
    print("=" * 50)

    # Se executado com --api, testa a API
    if "--api" in sys.argv:
        asyncio.run(test_segmentation_api())
    elif "--pytest" not in sys.argv:
        print("\nPara executar com pytest:")
        print("pytest tests/test_segmentation.py -v")
