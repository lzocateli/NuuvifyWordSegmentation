from typing import Optional

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

from src.core.config import settings


class AzureKeyVaultService:
    def __init__(self):
        self.client: Optional[SecretClient] = None
        self.connect_to_azure()

    def connect_to_azure(self) -> SecretClient:
        """Conecta ao Azure Key Vault"""
        try:
            credential = ClientSecretCredential(
                tenant_id=settings.AzureKeyVault__TenantId,
                client_id=settings.AzureKeyVault__ClientId,
                client_secret=settings.AzureKeyVault__ClientSecret,
            )

            self.client = SecretClient(
                vault_url=settings.AzureKeyVault__Dns.unicode_string(),
                credential=credential,
            )
            print("Conectado ao Azure Key Vault com sucesso")

        except Exception as e:
            print(f"Erro ao conectar ao Azure Key Vault: {e}")
            self.client = None

    def get_secret(self, secret_name: str) -> Optional[str]:
        """Recupera um segredo do Azure Key Vault"""
        if not self.client:
            print("Cliente do Azure Key Vault não inicializado")
            return None

        try:
            secret = self.client.get_secret(secret_name)
            return secret.value
        except Exception as e:
            print(f"Erro ao recuperar segredo '{secret_name}': {e}")
            return None


# Instância global do serviço
azure_service = AzureKeyVaultService()
