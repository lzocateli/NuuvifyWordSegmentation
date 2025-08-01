# Multi-stage build para produção
ARG BUILDPLATFORM=linux/amd64
ARG PYTHON_VERSION=3.12

# Stage 1: Build dependencies
FROM --platform=$BUILDPLATFORM lzocateli/devops:${PYTHON_VERSION}-bookworm as builder

# Instalar dependências de sistema necessárias para build
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Configurar Python para produção
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Criar usuário não-root para segurança
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copiar arquivos de configuração primeiro (cache layer)
COPY pyproject.toml ./

# Instalar dependências em ambiente virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip e instalar dependências
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

# Baixar modelo spaCy (pode ser demorado, melhor fazer no build)
RUN python -c "import spacy; spacy.cli.download('pt_core_news_lg')"

# Stage 2: Production image
FROM --platform=$BUILDPLATFORM lzocateli/devops:${PYTHON_VERSION}-bookworm as production

# Instalar apenas dependências de runtime
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Configurar Python para produção
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src:$PYTHONPATH"

# Criar usuário não-root
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copiar ambiente virtual do stage de build
COPY --from=builder /opt/venv /opt/venv

# Criar diretórios da aplicação
WORKDIR /app
RUN mkdir -p /app/src /app/tests && \
    chown -R appuser:appuser /app

# Copiar código fonte
COPY --chown=appuser:appuser src/ /app/src/
COPY --chown=appuser:appuser pyproject.toml /app/

# Mudar para usuário não-root
USER appuser

# Expor porta da aplicação
EXPOSE 8000

# Configuração de saúde
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Comando padrão para produção
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--access-log"]
