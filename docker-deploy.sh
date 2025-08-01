#!/bin/bash
# Script para build e deploy da aplicação Nuuvify

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configurações
APP_NAME="nuuvify-word-segmentation"
VERSION=${1:-"latest"}
REGISTRY=${DOCKER_REGISTRY:-""}

# Funções
show_help() {
    echo "Uso: $0 [VERSION] [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  build-dev     - Build imagem de desenvolvimento"
    echo "  build-prod    - Build imagem de produção"
    echo "  run-dev       - Executar em modo desenvolvimento"
    echo "  run-prod      - Executar em modo produção"
    echo "  test          - Executar testes"
    echo "  push          - Push para registry"
    echo "  deploy        - Deploy completo (build + push)"
    echo "  clean         - Limpar imagens antigas"
    echo "  help          - Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 v1.0.0 build-prod"
    echo "  $0 latest run-dev"
    echo "  $0 v1.0.0 deploy"
}

build_dev() {
    log_info "Building development image..."
    docker build -f Dockerfile.dev -t ${APP_NAME}:${VERSION}-dev .
    log_success "Development image built successfully"
}

build_prod() {
    log_info "Building production image..."
    docker build -f Dockerfile -t ${APP_NAME}:${VERSION} .
    log_success "Production image built successfully"
}

run_dev() {
    log_info "Starting development environment..."
    docker-compose up nuuvify-dev
}

run_prod() {
    log_info "Starting production environment..."
    docker-compose --profile production up -d
    log_success "Production environment started"
    log_info "API available at: http://localhost:8080"
    log_info "Health check: http://localhost:8080/api/v1/health"
}

run_tests() {
    log_info "Running tests..."
    docker build -f Dockerfile.dev -t ${APP_NAME}:test-${VERSION} .
    docker run --rm ${APP_NAME}:test-${VERSION} python -m pytest tests/ -v
    log_success "Tests completed"
}

push_images() {
    if [ -z "$REGISTRY" ]; then
        log_error "DOCKER_REGISTRY não definido. Defina a variável de ambiente."
        exit 1
    fi
    
    log_info "Pushing images to registry..."
    docker tag ${APP_NAME}:${VERSION} ${REGISTRY}/${APP_NAME}:${VERSION}
    docker push ${REGISTRY}/${APP_NAME}:${VERSION}
    
    if [ "$VERSION" != "latest" ]; then
        docker tag ${APP_NAME}:${VERSION} ${REGISTRY}/${APP_NAME}:latest
        docker push ${REGISTRY}/${APP_NAME}:latest
    fi
    
    log_success "Images pushed successfully"
}

deploy() {
    log_info "Starting deployment process..."
    build_prod
    run_tests
    if [ -n "$REGISTRY" ]; then
        push_images
    else
        log_warning "DOCKER_REGISTRY não definido. Pulando push."
    fi
    log_success "Deployment completed"
}

clean_images() {
    log_info "Cleaning old images..."
    docker image prune -f
    docker system prune -f
    log_success "Cleanup completed"
}

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    log_error "Docker não está rodando. Inicie o Docker e tente novamente."
    exit 1
fi

# Processar argumentos
case "${2:-build-prod}" in
    "build-dev")
        build_dev
        ;;
    "build-prod")
        build_prod
        ;;
    "run-dev")
        run_dev
        ;;
    "run-prod")
        run_prod
        ;;
    "test")
        run_tests
        ;;
    "push")
        push_images
        ;;
    "deploy")
        deploy
        ;;
    "clean")
        clean_images
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        log_error "Comando desconhecido: $2"
        show_help
        exit 1
        ;;
esac
