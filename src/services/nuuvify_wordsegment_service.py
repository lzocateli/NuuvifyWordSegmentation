import spacy


class WordSegmenter:
    def __init__(self):
        # Modelos carregados por idioma
        self.models = {}

        # Mapeamento de idiomas para modelos
        self.language_models = {"pt": "pt_core_news_lg", "en": "en_core_web_lg"}

        # Siglas que devem ser preservadas por idioma
        self.SIGLAS = {
            "pt": {"sp", "ti", "mg", "pi", "pr"},
            "en": {"usa", "uk", "ai", "it", "hr"},
        }

    def _get_model(self, language: str):
        """Carrega o modelo para o idioma especificado se ainda não estiver carregado"""
        if language not in self.models:
            if language not in self.language_models:
                raise ValueError(
                    f"Idioma '{language}' não suportado. Use 'pt' ou 'en'."
                )

            model_name = self.language_models[language]
            try:
                self.models[language] = spacy.load(model_name)
            except OSError:
                raise RuntimeError(
                    f"Modelo '{model_name}' não encontrado. "
                    "Certifique-se de que está instalado."
                )

        return self.models[language]

    def segment_and_format(self, text: str, language: str) -> str:
        """Segmenta e formata o texto usando NLP"""
        nlp = self._get_model(language)
        doc = nlp(text.lower())
        tokens = [t.text for t in doc if t.is_alpha]

        formatted = []
        siglas = self.SIGLAS.get(language, set())

        for token in tokens:
            if token in siglas:
                formatted.append(token.upper())
            else:
                formatted.append(token.capitalize())

        return "".join(formatted)

    async def check_connection_status(self) -> dict:
        """Verifica o status do serviço de segmentação"""
        try:
            # Teste simples para verificar se pelo menos um modelo pode ser carregado
            self._get_model("pt")  # Testa carregamento do modelo português
            return {
                "service": "word_segmentation",
                "status": "active",
                "model_loaded": True,
                "logged_in": True,  # Mantido para compatibilidade
            }
        except Exception:
            return {
                "service": "word_segmentation",
                "status": "error",
                "model_loaded": False,
                "logged_in": False,
            }

    async def disconnect(self) -> bool:
        """Método para compatibilidade - não há conexão para desconectar"""
        return True


# Instância global do serviço
nuuvify_wordsegment_service = WordSegmenter()
