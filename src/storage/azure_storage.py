from azure.storage.blob import BlobServiceClient
from .base import StorageProvider

class AzureStorage(StorageProvider):
    def __init__(self, connection_string, container_name):
        self.blob_service = BlobServiceClient.from_connection_string(connection_string)
        self.container = self.blob_service.get_container_client(container_name)
    
    def upload_file(self, file_data, file_name):
        blob_client = self.container.get_blob_client(file_name)
        blob_client.upload_blob(file_data.getvalue(), overwrite=True)
        return f"azure://{self.container.container_name}/{file_name}"
    
    def get_file_url(self, file_name):
        blob_client = self.container.get_blob_client(file_name)
        return blob_client.url