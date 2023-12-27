
# Minio Image Uploader

## Introduction
`MinioImageUploader` is a Python wrapper class for uploading images to a Minio S3 bucket and generating pre-signed URLs. These URLs provide temporary access to the uploaded images, making them ideal for secure, time-limited sharing.

## Installation

### Prerequisites
- Python 3.x
- Minio server (or AWS S3 compatible storage) access

### Steps
1. Install Minio Python client:
   ```
   pip install minio
   ```

## Usage

### Initialization
Create an instance of `MinioImageUploader` with your Minio server details:
```python
from minio_image_uploader import MinioImageUploader

uploader = MinioImageUploader('your-minio-endpoint', 'YOUR-ACCESSKEY', 'YOUR-SECRETKEY')
```

### Uploading Images
Upload an image to a specified bucket:
```python
image_url = uploader.upload_image('your-bucket-name', '/path/to/your/image.jpg')
print(image_url)
```

### Retrieving Image URL
Get a pre-signed URL for an existing image in the bucket:
```python
image_url = uploader.get_image_url('your-bucket-name', 'image.jpg')
print(image_url)
```

## Notes
- Ensure that your Minio server is properly configured and accessible.
- Replace `your-minio-endpoint`, `YOUR-ACCESSKEY`, `YOUR-SECRETKEY`, and `your-bucket-name` with your actual Minio server details and bucket name.
- The generated URLs are valid for a limited time (default is 5 minutes for `upload_image` and the duration specified in `get_image_url`).
- The `upload_image` method automatically sets the MIME type and tries to make the image viewable in the browser.
