import spacy


class WordSegmenter:
    def __init__(self):
        # Carrega modelo de português
        self.nlp = spacy.load("pt_core_news_sm")

        # Siglas que devem ser preservadas
        self.SIGLAS = {"sp", "ti", "mg", "pi", "pr"}

    def segment_and_format(self, text: str) -> str:
        """Segmenta e formata o texto usando NLP"""
        doc = self.nlp(text.lower())
        tokens = [t.text for t in doc if t.is_alpha]

        formatted = []
        for token in tokens:
            if token in self.SIGLAS:
                formatted.append(token.upper())
            else:
                formatted.append(token.capitalize())

        return "".join(formatted)

    async def check_connection_status(self) -> dict:
        """Verifica o status do serviço de segmentação"""
        try:
            # Teste simples para verificar se o modelo está carregado
            self.nlp("teste")
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
