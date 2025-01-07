import os
from pathlib import Path
from .base import StorageProvider

class LocalStorage(StorageProvider):
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
    
    def upload_file(self, file_data, file_name):
        file_path = self.upload_dir / file_name
        with open(file_path, "wb") as f:
            f.write(file_data.getvalue())
        return str(file_path)
    
    def get_file_url(self, file_name):
        return str(self.upload_dir / file_name)