"""
Testes unitários para o serviço de segmentação de palavras
"""

import pytest

from src.services.nuuvify_wordsegment_service import nuuvify_wordsegment_service


class TestWordSegmentationService:
    """Testes para o serviço de segmentação"""

    def test_service_initialization(self):
        """Testa se o serviço foi inicializado corretamente"""
        assert nuuvify_wordsegment_service is not None
        assert hasattr(nuuvify_wordsegment_service, "models")
        assert hasattr(nuuvify_wordsegment_service, "language_models")
        assert hasattr(nuuvify_wordsegment_service, "SIGLAS")

    def test_segment_and_format_basic(self):
        """Testa segmentação básica"""
        result = nuuvify_wordsegment_service.segment_and_format("casa", "pt")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_segment_and_format_basic_english(self):
        """Testa segmentação básica em inglês"""
        result = nuuvify_wordsegment_service.segment_and_format("house", "en")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_segment_and_format_with_acronyms(self):
        """Testa se as siglas são preservadas em maiúsculo"""
        test_cases = [
            ("sp", "SP"),
            ("ti", "TI"),
            ("mg", "MG"),
            ("pi", "PI"),
            ("pr", "PR"),
        ]

        for input_text, expected_acronym in test_cases:
            result = nuuvify_wordsegment_service.segment_and_format(input_text, "pt")
            assert expected_acronym in result

    def test_segment_and_format_with_english_acronyms(self):
        """Testa se as siglas em inglês são preservadas em maiúsculo"""
        test_cases = [
            ("usa", "USA"),
            ("uk", "UK"),
            ("ai", "AI"),
            ("it", "IT"),
            ("hr", "HR"),
        ]

        for input_text, expected_acronym in test_cases:
            result = nuuvify_wordsegment_service.segment_and_format(input_text, "en")
            assert expected_acronym in result

    def test_segment_and_format_complex_text(self, sample_texts):
        """Testa segmentação com textos mais complexos"""
        for text in sample_texts:
            result = nuuvify_wordsegment_service.segment_and_format(text, "pt")

            # Verificações básicas
            assert isinstance(result, str)
            assert len(result) > 0
            assert len(result) >= len(text.lower())  # Não deve ficar menor

            # Deve começar com letra maiúscula
            assert result[0].isupper()

    @pytest.mark.asyncio
    async def test_check_connection_status(self):
        """Testa verificação de status do serviço"""
        status = await nuuvify_wordsegment_service.check_connection_status()

        assert isinstance(status, dict)
        assert "service" in status
        assert "status" in status
        assert "model_loaded" in status
        assert status["service"] == "word_segmentation"

    @pytest.mark.asyncio
    async def test_disconnect_method(self):
        """Testa método de desconexão"""
        result = await nuuvify_wordsegment_service.disconnect()
        assert isinstance(result, bool)
        assert result is True  # Sempre retorna True por compatibilidade

    def test_empty_string_handling(self):
        """Testa comportamento com string vazia"""
        result = nuuvify_wordsegment_service.segment_and_format("", "pt")
        assert isinstance(result, str)

    def test_special_characters_handling(self):
        """Testa comportamento com caracteres especiais"""
        test_cases = [
            "casa123",
            "casa!@#",
            "casa-azul",
            "casa_grande",
        ]

        for text in test_cases:
            result = nuuvify_wordsegment_service.segment_and_format(text, "pt")
            assert isinstance(result, str)
            # Deve filtrar apenas caracteres alfabéticos
            assert all(c.isalpha() for c in result)

    def test_invalid_language_parameter(self):
        """Testa comportamento com idioma inválido"""
        with pytest.raises(ValueError) as exc_info:
            nuuvify_wordsegment_service.segment_and_format("test", "fr")
        assert "não suportado" in str(exc_info.value)
