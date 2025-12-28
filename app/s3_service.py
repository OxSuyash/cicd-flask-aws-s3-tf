import boto3
from botocore.exceptions import ClientError
import os

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
s3 = boto3.client("s3")

def upload_text_file(filename: str, content: str):
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=filename, Body=content)
        return True
    except ClientError as e:
        print(e)
        return False

def list_files():
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        if "Contents" not in response:
            return []
        return [obj["Key"] for obj in response["Contents"]]
    except ClientError as e:
        print(e)
        return []


def generate_download_url(filename: str, expires_in=300):
    try:
        url = s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": filename
            },
            ExpiresIn=expires_in
        )
        return url
    except ClientError as e:
        print(e)
        return None
