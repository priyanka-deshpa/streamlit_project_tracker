from abc import ABC, abstractmethod

class StorageProvider(ABC):
    @abstractmethod
    def upload_file(self, file_data, file_name):
        pass
    
    @abstractmethod
    def get_file_url(self, file_name):
        pass