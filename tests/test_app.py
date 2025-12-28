# # tests/test_app.py
# import pytest
# from unittest.mock import patch, MagicMock
# import app.s3_service as s3_service

# @pytest.fixture
# def mock_s3_client():
#     with patch("app.s3_service.boto3.client") as mock_client:
#         yield mock_client

# def test_upload_text_file_success(mock_s3_client):
#     mock_instance = MagicMock()
#     mock_s3_client.return_value = mock_instance
#     mock_instance.put_object.return_value = {}

#     result = s3_service.upload_text_file("test.txt", "hello")
#     assert result is True
#     mock_instance.put_object.assert_called_once_with(
#         Bucket=s3_service.BUCKET_NAME,
#         Key="test.txt",
#         Body="hello"
#     )

# def test_upload_text_file_failure(mock_s3_client):
#     mock_instance = MagicMock()
#     mock_s3_client.return_value = mock_instance
#     mock_instance.put_object.side_effect = Exception("S3 error")

#     result = s3_service.upload_text_file("test.txt", "hello")
#     assert result is False

# def test_list_files_with_contents(mock_s3_client):
#     mock_instance = MagicMock()
#     mock_s3_client.return_value = mock_instance
#     mock_instance.list_objects_v2.return_value = {
#         "Contents": [{"Key": "file1.txt"}, {"Key": "file2.txt"}]
#     }

#     result = s3_service.list_files()
#     assert result == ["file1.txt", "file2.txt"]

# def test_list_files_empty(mock_s3_client):
#     mock_instance = MagicMock()
#     mock_s3_client.return_value = mock_instance
#     mock_instance.list_objects_v2.return_value = {}

#     result = s3_service.list_files()
#     assert result == []

# def test_generate_download_url_success(mock_s3_client):
#     mock_instance = MagicMock()
#     mock_s3_client.return_value = mock_instance
#     mock_instance.generate_presigned_url.return_value = "http://signed-url"

#     url = s3_service.generate_download_url("file.txt")
#     assert url == "http://signed-url"
#     mock_instance.generate_presigned_url.assert_called_once()

# def test_generate_download_url_failure(mock_s3_client):
#     mock_instance = MagicMock()
#     mock_s3_client.return_value = mock_instance
#     mock_instance.generate_presigned_url.side_effect = Exception("S3 error")

#     url = s3_service.generate_download_url("file.txt")
#     assert url is None
