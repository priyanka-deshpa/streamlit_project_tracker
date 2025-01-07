import os
from dotenv import load_dotenv
from .local_storage import LocalStorage
from .s3_storage import S3Storage
from .azure_storage import AzureStorage

load_dotenv()

def get_storage_provider(provider_name):
    if provider_name == "local":
        return LocalStorage()
    elif provider_name == "s3":
        return S3Storage(
            bucket_name=os.getenv("AWS_BUCKET_NAME"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
    elif provider_name == "azure":
        return AzureStorage(
            connection_string=os.getenv("AZURE_CONNECTION_STRING"),
            container_name=os.getenv("AZURE_CONTAINER_NAME")
        )
    else:
        raise ValueError(f"Unsupported storage provider: {provider_name}")