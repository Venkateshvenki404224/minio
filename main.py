from minio import Minio
from minio.error import S3Error
import os
from datetime import timedelta
from urllib.parse import quote
import mimetypes

class MinioImageUploader:
    def __init__(self, endpoint, access_key, secret_key):
        # Initialize minio client with an endpoint and access/secret keys.
        self.client = Minio(endpoint,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=True)  # Change to True for HTTPS


    def get_image_url(self, bucket_name, file_name):
        # Check if the file exists in the bucket
        try:
            self.client.stat_object(bucket_name, file_name)
        except S3Error as exc:
            print(f"Error occurred: {exc}")
            return None

        # Set the Content-Disposition to inline for browser viewing
        content_disposition = f"inline; filename*=utf-8''{quote(file_name)}"
        response_headers = {"Response-Content-Disposition": content_disposition}

        # Generate a presigned URL for the image, valid for 5 minutes
        return self.client.presigned_get_object(
            bucket_name, file_name, expires=timedelta(minutes=1), response_headers=response_headers
        )
        

    def upload_image(self, bucket_name, file_path):
        # Ensure the bucket exists
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)

        # File name in the bucket is derived from the file path
        file_name = os.path.basename(file_path)
        content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
        try:
            # Upload the image
            self.client.fput_object(bucket_name, file_name, file_path, content_type=content_type)
            print(f"File {file_path} is successfully uploaded as {file_name}")
        except S3Error as exc:
            print("Error occurred: ", exc)
            return None
        
        # Set the Content-Disposition to inline for browser viewing
        content_disposition = f"inline; filename*=utf-8''{quote(file_name)}"
        response_headers = {"Response-Content-Disposition": content_disposition}

        # Generate a presigned URL for the uploaded image, valid for 5 minutes
        return self.client.presigned_get_object(
            bucket_name, file_name, expires=timedelta(minutes=1), response_headers=response_headers
        )

# Usage example
uploader = MinioImageUploader('endpoint', 'access_key', 'secret_key')
image_url = uploader.get_image_url('bucket_name', 'image.jpg')
print(image_url)
