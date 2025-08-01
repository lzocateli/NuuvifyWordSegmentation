#!/usr/bin/env python3
"""
Script para executar os testes do projeto Nuuvify Word Segmentation
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Executa um comando e exibe o resultado"""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ {description} - SUCESSO")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FALHOU")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Função principal"""
    print("🧪 EXECUTANDO TESTES - NUUVIFY WORD SEGMENTATION")

    # Verificar se está no diretório correto
    if not os.path.exists("pyproject.toml"):
        print("❌ Execute este script a partir da raiz do projeto")
        sys.exit(1)

    success_count = 0
    total_tests = 0

    # Lista de testes para executar
    tests = [
        {
            "command": "python -m pytest tests/test_word_segmentation_service.py -v",
            "description": "Testes Unitários do Serviço",
        },
        {
            "command": "python -m pytest tests/test_segmentation.py::TestWordSegmentation::test_local_segmentation -v",
            "description": "Testes Locais de Segmentação",
        },
    ]

    # Testes que requerem API rodando
    api_tests = [
        {
            "command": "python -m pytest tests/test_segmentation.py::TestWordSegmentation::test_segmentation_api_status -v",
            "description": "Testes de Status da API",
        },
        {
            "command": "python -m pytest tests/test_segmentation.py::TestWordSegmentation::test_segmentation_api_endpoint -v",
            "description": "Testes de Endpoint da API",
        },
    ]

    # Executar testes que não precisam da API
    for test in tests:
        total_tests += 1
        if run_command(test["command"], test["description"]):
            success_count += 1

    # Verificar se a API está rodando para testes de integração
    print(f"\n{'='*50}")
    print("🌐 Verificando se a API está rodando...")
    print(f"{'='*50}")

    try:
        import asyncio

        import httpx

        async def check_api():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "http://localhost:8000/api/v1/", timeout=2
                    )
                    return response.status_code == 200
            except:
                return False

        api_running = asyncio.run(check_api())

        if api_running:
            print("✅ API está rodando - executando testes de integração")
            for test in api_tests:
                total_tests += 1
                if run_command(test["command"], test["description"]):
                    success_count += 1
        else:
            print("⚠️  API não está rodando - pulando testes de integração")
            print("   Para executar testes completos:")
            print("   1. uvicorn src.api.main:app --reload")
            print("   2. python run_tests.py")

    except ImportError:
        print("⚠️  httpx não disponível - pulando verificação da API")

    # Executar linting se disponível
    linting_tests = [
        {
            "command": "python -m black --check src/ tests/",
            "description": "Verificação de Formatação (Black)",
        },
        {
            "command": "python -m ruff check src/ tests/",
            "description": "Linting (Ruff)",
        },
    ]

    print(f"\n{'='*50}")
    print("🔍 Executando verificações de qualidade...")
    print(f"{'='*50}")

    for test in linting_tests:
        # Não conta como teste obrigatório
        run_command(test["command"], test["description"])

    # Resumo
    print(f"\n{'='*60}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*60}")
    print(f"✅ Sucessos: {success_count}/{total_tests}")
    print(f"❌ Falhas: {total_tests - success_count}/{total_tests}")

    if success_count == total_tests:
        print("🎉 TODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        sys.exit(1)


if __name__ == "__main__":
    main()
