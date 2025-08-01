"""
Configurações para testes da API Nuuvify
"""

import sys
from pathlib import Path

import pytest

# Adicionar o diretório raiz do projeto ao sys.path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


@pytest.fixture(scope="session")
def api_base_url():
    """URL base da API para testes"""
    return "http://localhost:8000"


@pytest.fixture
def sample_texts():
    """Textos de exemplo para testes"""
    return [
        "minhacasatemsp",
        "euamoobrasilsp",
        "sistemadeinformacaomg",
        "tecnologiadainformacaoti",
        "belahoraparasegmentarpr",
    ]


@pytest.fixture
def expected_patterns():
    """Padrões esperados nos resultados"""
    return {
        "has_capital_letters": True,
        "preserves_acronyms": ["SP", "TI", "MG", "PI", "PR"],
        "min_length": 1,
    }
