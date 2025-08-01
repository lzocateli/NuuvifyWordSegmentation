#!/usr/bin/env python3
"""
Exemplo de uso da API de segmentação de palavras com suporte a idiomas
"""

import asyncio

import httpx


async def test_segmentation_examples():
    """Exemplos de uso da API de segmentação"""
    base_url = "http://localhost:8000"

    # Exemplos em português
    portuguese_examples = [
        {"text": "minhacasatemsp", "language": "pt"},
        {"text": "euamoobrasilsp", "language": "pt"},
        {"text": "sistemadeinformacaomg", "language": "pt"},
        {"text": "tecnologiadainformacaoti", "language": "pt"},
    ]

    # Exemplos em inglês
    english_examples = [
        {"text": "myhouseisbeautiful", "language": "en"},
        {"text": "artificialintelligenceusa", "language": "en"},
        {"text": "informationtechnologyuk", "language": "en"},
        {"text": "humanresourceshr", "language": "en"},
    ]

    async with httpx.AsyncClient() as client:
        print("🧪 Testando Segmentação de Palavras com Suporte a Idiomas\n")

        print("📝 Exemplos em Português:")
        print("-" * 40)
        for example in portuguese_examples:
            try:
                response = await client.post(
                    f"{base_url}/api/v1/segment/", json=example
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ '{example['text']}' → '{result['formatted']}'")
                else:
                    print(f"❌ Erro: {response.status_code} - {response.text}")

            except Exception as e:
                print(f"❌ Erro: {e}")

        print("\n📝 Exemplos em Inglês:")
        print("-" * 40)
        for example in english_examples:
            try:
                response = await client.post(
                    f"{base_url}/api/v1/segment/", json=example
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ '{example['text']}' → '{result['formatted']}'")
                else:
                    print(f"❌ Erro: {response.status_code} - {response.text}")

            except Exception as e:
                print(f"❌ Erro: {e}")


def test_local_examples():
    """Testa localmente sem a API"""
    print("🔧 Testando Localmente\n")

    try:
        from src.services.nuuvify_wordsegment_service import nuuvify_wordsegment_service

        print("📝 Exemplos em Português:")
        print("-" * 40)
        portuguese_texts = ["minhacasatemsp", "euamoobrasilsp", "sistemadeinformacaomg"]

        for text in portuguese_texts:
            result = nuuvify_wordsegment_service.segment_and_format(text, "pt")
            print(f"✅ '{text}' → '{result}'")

        print("\n📝 Exemplos em Inglês:")
        print("-" * 40)
        english_texts = [
            "myhouseisbeautiful",
            "artificialintelligenceusa",
            "informationtechnologyuk",
        ]

        for text in english_texts:
            result = nuuvify_wordsegment_service.segment_and_format(text, "en")
            print(f"✅ '{text}' → '{result}'")

        print("\n📝 Testando idioma inválido:")
        print("-" * 40)
        try:
            result = nuuvify_wordsegment_service.segment_and_format("test", "fr")
            print(f"✅ 'test' → '{result}'")
        except ValueError as e:
            print(f"❌ Erro esperado: {e}")

    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("EXEMPLO DE USO - SEGMENTAÇÃO COM SUPORTE A IDIOMAS")
    print("=" * 60 + "\n")

    # Teste local
    test_local_examples()

    print("\n" + "=" * 60)
    print("Para testar a API, execute:")
    print("1. uvicorn src.api.main:app --reload")
    print("2. python example_usage.py --api")
    print("=" * 60)

    # Se executado com --api, testa a API
    import sys

    if "--api" in sys.argv:
        asyncio.run(test_segmentation_examples())
