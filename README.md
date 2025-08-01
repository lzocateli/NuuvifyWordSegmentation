# API de Segmentação de Palavras Nuuvify

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![spaCy](https://img.shields.io/badge/spaCy-NLP-orange.svg)

API FastAPI para segmentação e formatação de palavras usando NLP com spaCy.

> 🐳 **Recomendado**: Use Docker para execução rápida e sem problemas de dependências!

## 📋 Pré-requisitos

### Para Docker (Recomendado) 🐳
- **Docker** (obrigatório)
- **Git** (para clone do repositório)

### Para Instalação Local (Alternativa) 🐍  
- **Python 3.11+** (obrigatório)
- **Git** (para clone do repositório)

### Verificação Rápida
```bash
# Verificar Docker
docker --version

# Verificar Python (se não usar Docker)
python --version

# Verificação automática completa
python check_requirements.py
```

## ⚡ Início Rápido

```bash
# 1. Clone o repositório
git clone <repository>
cd NuuvifyWordSegmentarion

# 2. Execute com Docker (RECOMENDADO)
./docker-deploy.sh latest run-dev
# API disponível em: http://localhost:8000

# 3. Teste a API
curl -X POST "http://localhost:8000/api/v1/segment/" \
     -H "Content-Type: application/json" \
     -d '{"text": "minhacasatemsp"}'

# 4. Acesse a documentação
# http://localhost:8000/docs
```

### Por que Docker? 🐳

- ✅ **Zero configuração** - Funciona imediatamente
- ✅ **Isolamento** - Não afeta seu sistema
- ✅ **Consistência** - Mesmo ambiente em qualquer máquina
- ✅ **Produção-ready** - Deploy direto para produção
- ✅ **Performance** - Otimizado para alta performance
- ✅ **Dependências** - Modelo spaCy já incluído

## 🚀 Execução

### Método Recomendado - Docker

```bash
# Desenvolvimento (com hot reload)
./docker-deploy.sh latest run-dev

# Produção
./docker-deploy.sh v1.0.0 run-prod

# Build e deploy completo
./docker-deploy.sh v1.0.0 deploy
```

### Método Alternativo - Instalação Local

#### Instalação das dependências

```bash
# Usando uv (mais rápido - requer instalação)
# Instalar uv primeiro:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Em seguida:
uv venv
source .venv/bin/activate && uv pip install -e .

```

### Executar o servidor

```bash
# Usando uvicorn diretamente
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Ou usando o módulo Python
python -m uvicorn src.api.main:app --reload
```

### Parar o servidor

```bash
# Método 1: Ctrl+C no terminal onde o servidor está rodando
# Pressione Ctrl+C

# Método 2: Parar processo uvicorn
pkill -f "uvicorn src.api.main:app"

# Método 3: Parar por PID específico
ps aux | grep uvicorn  # encontrar o PID
kill <PID>             # substituir <PID> pelo número do processo
```

## 📋 Endpoints Disponíveis

### 1. Endpoint Principal
- **GET** `/api/v1/` - Boas-vindas à API

### 2. Status e Health
- **GET** `/api/v1/status` - Status da API
- **GET** `/api/v1/health` - Health check completo

### 3. Segmentação de Palavras
- **POST** `/api/v1/segment/` - Segmenta e formata texto

**Exemplo de uso:**

```bash
curl -X POST "http://localhost:8000/api/v1/segment/" \
     -H "Content-Type: application/json" \
     -d '{"text": "minhacasatemsp"}'
```

**Resposta:**
```json
{
  "original": "minhacasatemsp",
  "formatted": "MinhaCasaTemSP"
}
```

### 4. Autenticação
- **POST** `/api/v1/auth/login` - Login básico
- **GET** `/api/v1/auth/status` - Status da autenticação

## 🧪 Testes

### Executar testes com pytest

```bash
# Executar todos os testes
pytest tests/ -v

# Executar testes específicos
pytest tests/test_word_segmentation_service.py -v

# Executar com cobertura
pytest tests/ --cov=src --cov-report=html

# Executar testes de API (servidor deve estar rodando)
pytest tests/test_segmentation.py::TestWordSegmentation::test_segmentation_api_endpoint -v
```

### Executar script de teste manual

```bash
# Script automatizado (recomendado)
python run_tests.py

# Teste local (sem servidor)
python tests/test_segmentation.py

# Teste completo com API (servidor deve estar rodando)
python tests/test_segmentation.py --api
```

### Executar servidor para testes

```bash
# Terminal 1: Iniciar servidor
uvicorn src.api.main:app --reload

# Terminal 2: Executar testes de API
pytest tests/test_segmentation.py -v
```

## 📖 Documentação Interativa

Acesse a documentação interativa:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Funcionalidades

- Segmentação inteligente de palavras usando NLP
- Preservação de siglas conhecidas (SP, TI, MG, PI, PR)
- Capitalização automática das palavras
- API RESTful com FastAPI
- Documentação automática
- Health checks
- Logs estruturados

## 🔧 Desenvolvimento

### Estrutura do Projeto

```
src/
├── api/              # Rotas e aplicação FastAPI
│   ├── main.py       # Aplicação principal
│   ├── routes.py     # Rotas gerais
│   ├── auth_routes.py        # Autenticação
│   └── nuuvify_wordsegment_routes.py  # Segmentação
├── core/             # Configurações e modelos
│   ├── config.py     # Configurações
│   └── models.py     # Modelos Pydantic
└── services/         # Lógica de negócio
    └── nuuvify_wordsegment_service.py  # Serviço de segmentação
tests/                # Testes automatizados
├── __init__.py       # Inicialização do pacote de testes
├── conftest.py       # Configurações de testes
├── test_segmentation.py  # Testes de integração da API
└── test_word_segmentation_service.py  # Testes unitários
```

### Linting e Formatação

```bash
# Formatação com black
black src/

# Linting com ruff
ruff check src/

# Type checking com mypy
mypy src/
```

## 🐳 Docker

### Build e Execução

#### Desenvolvimento
```bash
# Build imagem de desenvolvimento
./docker-deploy.sh latest build-dev

# Executar em modo desenvolvimento (com reload)
./docker-deploy.sh latest run-dev

# Ou usando docker-compose diretamente
docker-compose up nuuvify-dev
```

#### Produção
```bash
# Build imagem de produção
./docker-deploy.sh v1.0.0 build-prod

# Executar em modo produção
./docker-deploy.sh v1.0.0 run-prod

# Ou usando docker-compose
docker-compose --profile production up -d
```

#### Deploy Completo
```bash
# Deploy com testes automáticos
./docker-deploy.sh v1.0.0 deploy

# Limpar imagens antigas
./docker-deploy.sh latest clean
```

### Estrutura Docker

- `Dockerfile` - Imagem otimizada para produção (multi-stage build)
- `Dockerfile.dev` - Imagem para desenvolvimento
- `docker-compose.yml` - Orquestração completa
- `nginx.conf` - Configuração do Nginx para produção
- `.dockerignore` - Otimização de build

### Características da Imagem de Produção

- ✅ Multi-stage build para reduzir tamanho
- ✅ Usuário não-root para segurança
- ✅ Health checks configurados
- ✅ Otimizações de cache do Docker
- ✅ Variables de ambiente para configuração
- ✅ Logs estruturados
- ✅ Múltiplos workers Uvicorn

## � Como Usar

## 🚀 Como Usar

### 🐳 Docker (Recomendado)

```bash
# Desenvolvimento com reload automático
./docker-deploy.sh latest run-dev
# API disponível em: http://localhost:8000

# Produção
./docker-deploy.sh v1.0.0 run-prod
# API disponível em: http://localhost:8080

# Com Nginx (proxy reverso)
docker-compose --profile nginx up -d
# API disponível em: http://localhost
```

### 🐍 Instalação Local (Alternativa)

```bash
# 1. Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -e .

# 3. Baixar modelo spaCy
python -c "import spacy; spacy.cli.download('pt_core_news_lg')"

# 4. Executar servidor
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Teste Rápido da API

```bash
# Testar segmentação
curl -X POST "http://localhost:8000/api/v1/segment/" \
     -H "Content-Type: application/json" \
     -d '{"text": "minhacasatemsp"}'

# Verificar saúde da API
curl http://localhost:8000/api/v1/health

# Acessar documentação
# http://localhost:8000/docs
```

### Executar Testes

```bash
# 🐳 Com Docker (recomendado)
./docker-deploy.sh latest test

# 🐍 Script automatizado local
python run_tests.py

# 🧪 Pytest direto
pytest tests/ -v
```

## �🔑 Configuração

### Variáveis de Ambiente

Copie `.env.example` para `.env` e configure as variáveis:

```bash
cp .env.example .env
```

**Principais configurações:**

- `DEBUG`: Modo debug (default: False)
- `API_PREFIX`: Prefixo da API (default: /api/v1)
- `SECRET_KEY`: Chave secreta para JWT
- `UVICORN_WORKERS`: Número de workers (default: 4)
- Azure Key Vault settings (opcionais)

### Docker Registry

Para push automático para registry:

```bash
export DOCKER_REGISTRY=your-registry.azurecr.io
./docker-deploy.sh v1.0.0 deploy
```

### Nginx (Produção)

O arquivo `nginx.conf` já está configurado com:

- Rate limiting
- Gzip compression
- Security headers
- Health checks
- Proxy para API

```bash
# Executar com Nginx
docker-compose --profile nginx up -d
```

**Endpoints disponíveis:**
- `http://localhost/api/` - API endpoints
- `http://localhost/docs` - Documentação Swagger
- `http://localhost/health` - Health check

## 🛠️ Resolução de Problemas

### Problemas Comuns

#### 1. Script de deploy não executa
```bash
# Solução: Tornar executável
chmod +x docker-deploy.sh
./docker-deploy.sh latest run-dev
```

#### 2. Docker não está rodando
```bash
# Solução: Iniciar Docker
# Linux/macOS: sudo systemctl start docker
# Windows: Iniciar Docker Desktop
# Ou usar instalação local:
pip install -e . && uvicorn src.api.main:app --reload
```

#### 3. `zsh: command not found: uv` (instalação local)
```bash
# Solução: Instalar uv ou usar pip
curl -LsSf https://astral.sh/uv/install.sh | sh
# Ou usar pip diretamente:
pip install -e .
```

#### 4. `ModuleNotFoundError: No module named 'spacy'` (instalação local)
```bash
# Solução: Instalar dependências
pip install -e .
```

#### 5. `OSError: [E050] Can't find model 'pt_core_news_lg'` (instalação local)
```bash
# Solução: Baixar modelo spaCy
python -c "import spacy; spacy.cli.download('pt_core_news_lg')"
```

#### 6. `Permission denied: docker`
```bash
# Solução: Adicionar usuário ao grupo docker (Linux)
sudo usermod -a -G docker $USER
# Logout e login novamente
```

#### 7. Porta já em uso
```bash
# Docker: usar porta diferente
docker-compose up nuuvify-dev -p 8001:8000
# Local: usar porta diferente
uvicorn src.api.main:app --reload --port 8001
```

#### 8. Como parar o servidor uvicorn
```bash
# Método mais comum: Ctrl+C no terminal ativo
# Pressione Ctrl+C onde o servidor está rodando

# Parar processo uvicorn por nome
pkill -f "uvicorn src.api.main:app"

# Parar todos os processos Python
pkill -f python

# Encontrar e matar processo específico
ps aux | grep uvicorn
kill <PID>  # usar o PID encontrado
```

### Verificação de Instalação

Execute o script de verificação:
```bash
python check_requirements.py
```

### Logs e Debug

```bash
# 🐳 Docker (recomendado)
docker-compose logs -f nuuvify-dev

# 🐍 Local com logs detalhados
uvicorn src.api.main:app --reload --log-level debug
```