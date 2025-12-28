# app/routes.py
from flask import Blueprint, jsonify, request
from app.s3_service import upload_text_file, list_files
from app.s3_service import generate_download_url


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return "Flask app is running"

@main.route("/health")
def health():
    return "OK"

@main.route("/test")
def test():
    return "This route was added to test pipeline trigger."

@main.route("/upload", methods=["POST"])
def upload():
    data = request.json
    filename = data["filename"]
    content = data["content"]

    success = upload_text_file(filename, content)

    return jsonify({"status": "uploaded" if success else "failed"})

@main.route("/files", methods=["GET"])
def files():
    return jsonify(list_files())

@main.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    url = generate_download_url(filename)
    if not url:
        return jsonify({"error": "Failed to generate URL"}), 500

    return jsonify({"download_url": url})


#hit endpoints
# POST /upload
# {
#   "filename": "test.txt",
#   "content": "Hello S3"
# }

#GET /files