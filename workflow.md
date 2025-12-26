



1. Create ec2 instance with s3 and iam Ref  ->   https://github.com/OxSuyash/create-ec2-iam-s3-tf

2. Create flask app locally
   Folder structure -
   ```
   flask-app/
    ├─ app/
    │  ├─ __init__.py
    │  ├─ routes.py
    │  └─ s3_service.py
    ├─ tests/
    │  └─ test_app.py
    ├─ docker-file/
    │  └─ Dockerfile
    ├─ run.py
    ├─ .gitignore
    └─ .env
   ```
   
3. Install dependencies
   ```
    pip install boto3
    pip install python-dotenv
   ```

4. Create Access key in aws, add it in .env. Delete access key once app is deployed on instance. This is development .env
   ```
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_REGION=
    S3_BUCKET_NAME=
    FLASK_HOST=
    FLASK_PORT=
   ```

5. When you want to deploy app on instance, you only need to provide FLASK_HOST, FLASK_PORT, S3_BUCKET_NAME, AWS_REGION.

     We can provide these env vars while running docker container for that app
       ```
        docker run -d -p 5000:5000 \
        -e FLASK_HOST=0.0.0.0 \
        -e FLASK_PORT=5000 \
        -e S3_BUCKET_NAME=my-bucket \
        -e AWS_REGION=us-east-1\
         your-image-name
       ```
      While developing, we are using localhost, but in prod FLASK_HOST=0.0.0.0 

      It makes app accessible from public ip or container port

6. Run app ```python run.py```

     hit endpoints "/" -> ``` Flask app running ```or "/files" -> empty list, since there are no files in s3 bucket

     - Use postman to hit "/upload"  ->  "/files"  -> will show list of files you uploaded.
      














