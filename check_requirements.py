#!/usr/bin/env python3
"""
Script para verificar pré-requisitos do projeto Nuuvify Word Segmentation
"""

import shutil
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Verifica a versão do Python"""
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ é obrigatório")
        return False
    else:
        print("✅ Versão do Python adequada")
        return True


def check_pip():
    """Verifica se pip está disponível"""
    try:
        import pip

        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"], capture_output=True, text=True
        )
        print(f"📦 pip: {result.stdout.strip()}")
        print("✅ pip disponível")
        return True
    except ImportError:
        print("❌ pip não está disponível")
        return False


def check_docker():
    """Verifica se Docker está disponível"""
    if shutil.which("docker"):
        try:
            result = subprocess.run(
                ["docker", "--version"], capture_output=True, text=True
            )
            print(f"🐳 Docker: {result.stdout.strip()}")

            # Verificar se Docker está rodando
            result = subprocess.run(["docker", "info"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Docker disponível e rodando")
                return True
            else:
                print("⚠️  Docker instalado mas não está rodando")
                return False
        except subprocess.CalledProcessError:
            print("⚠️  Docker instalado mas com problemas")
            return False
    else:
        print("⚠️  Docker não encontrado (opcional)")
        return False


def check_git():
    """Verifica se Git está disponível"""
    if shutil.which("git"):
        try:
            result = subprocess.run(
                ["git", "--version"], capture_output=True, text=True
            )
            print(f"📂 Git: {result.stdout.strip()}")
            print("✅ Git disponível")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Git instalado mas com problemas")
            return False
    else:
        print("⚠️  Git não encontrado (recomendado)")
        return False


def check_uv():
    """Verifica se uv está disponível"""
    if shutil.which("uv"):
        try:
            result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
            print(f"⚡ uv: {result.stdout.strip()}")
            print("✅ uv disponível (instalação mais rápida)")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  uv instalado mas com problemas")
            return False
    else:
        print("ℹ️  uv não encontrado (opcional - acelera instalação)")
        print("   Para instalar: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False


def check_project_structure():
    """Verifica a estrutura do projeto"""
    required_files = [
        "pyproject.toml",
        "src/api/main.py",
        "src/services/nuuvify_wordsegment_service.py",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)

    if missing_files:
        print("❌ Arquivos do projeto faltando:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Estrutura do projeto correta")
        return True


def main():
    """Função principal"""
    print("🔍 VERIFICAÇÃO DE PRÉ-REQUISITOS - NUUVIFY WORD SEGMENTATION")
    print("=" * 60)

    # Verificar Docker primeiro (método recomendado)
    print("\n📋 Verificando Docker (RECOMENDADO)...")
    docker_available = check_docker()

    if docker_available:
        print("\n🎉 Docker disponível! Método recomendado pronto para uso.")
        print("\n🚀 EXECUTE AGORA:")
        print("./docker-deploy.sh latest run-dev")
        print("# API disponível em: http://localhost:8000")
        print("\n📖 Documentação: http://localhost:8000/docs")
        return True

    print("\n📋 Docker não disponível. Verificando instalação local...")

    checks = [
        ("Python 3.11+", check_python_version, True),
        ("pip", check_pip, True),
        ("Estrutura do projeto", check_project_structure, True),
        ("Git", check_git, False),
        ("uv (opcional)", check_uv, False),
    ]

    results = []

    for name, check_func, required in checks:
        print(f"\n📋 Verificando {name}...")
        result = check_func()
        results.append((name, result, required))

    print("\n" + "=" * 60)
    print("📊 RESUMO (Instalação Local):")

    required_passed = 0
    required_total = 0
    optional_passed = 0
    optional_total = 0

    for name, passed, required in results:
        status = "✅" if passed else "❌"
        category = "OBRIGATÓRIO" if required else "OPCIONAL"
        print(f"{status} {name} ({category})")

        if required:
            required_total += 1
            if passed:
                required_passed += 1
        else:
            optional_total += 1
            if passed:
                optional_passed += 1

    print(f"\n📈 Obrigatórios: {required_passed}/{required_total}")
    print(f"\n📈 Opcionais: {optional_passed}/{optional_total}")

    if required_passed == required_total:
        print("\n🎉 Pré-requisitos para instalação local atendidos!")
        print("\n🚀 Próximos passos (Instalação Local):")
        print("1. pip install -e .")
        print("2. python -c \"import spacy; spacy.cli.download('pt_core_news_lg')\"")
        print("3. uvicorn src.api.main:app --reload")
        print("\n💡 DICA: Para uma experiência melhor, instale Docker e use:")
        print("./docker-deploy.sh latest run-dev")
        return True
    else:
        print("\n⚠️  Alguns pré-requisitos obrigatórios não foram atendidos.")
        print(
            "Resolva os problemas acima ou instale Docker para usar o método recomendado."
        )
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
