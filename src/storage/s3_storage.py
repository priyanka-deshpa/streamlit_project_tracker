import boto3
from .base import StorageProvider

class S3Storage(StorageProvider):
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.bucket = bucket_name
    
    def upload_file(self, file_data, file_name):
        self.s3.upload_fileobj(file_data, self.bucket, file_name)
        return f"s3://{self.bucket}/{file_name}"
    
    def get_file_url(self, file_name):
        return self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket, 'Key': file_name},
            ExpiresIn=3600
        )