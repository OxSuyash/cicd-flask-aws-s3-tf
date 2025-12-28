



1. Create ec2 instance with s3 and iam Ref  ->   https://github.com/OxSuyash/create-ec2-iam-s3-tf

      Read carefully main.tf, what resources are created and why
      Also read this  ->   https://github.com/OxSuyash/aws-notes/blob/main/public-vs-private.md

3. Create flask app locally
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
    ├─ requirements.txt
    ├─ .gitignore
    └─ .env
   
   ```
   
4. Install dependencies
   ```
    pip install boto3
    pip install python-dotenv
   ```

5. Create Access key in aws, add it in .env. Delete access key once app is deployed on instance. This is development .env

   Note: We cannot modify env var names later, because we will use them in project. But, in jenkins, global properties -> env vars are accessible to every pipeline.

   So, to isolate one project env vars from other project env vars  ->  we will add project name in env var name for unique identification of project env vars.

   Eg. ->  FLASK-APP-FLASK-HOST , E-COMM-APP-FLASK-PORT 
   ```
    AWS_ACCESS_KEY_ID=
    AWS_SECRET_ACCESS_KEY=
    AWS_REGION=
    S3_BUCKET_NAME=
    FLASK_HOST=
    FLASK_PORT=
   ```

7. When you want to deploy app on instance, you only need to provide FLASK_HOST, FLASK_PORT, S3_BUCKET_NAME, AWS_REGION.

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

8. Run app ```python run.py```

     hit endpoints "/" -> ``` Flask app running ```or "/files" -> empty list, since there are no files in s3 bucket

      /download/file_name   ->  gives url to download the file

     - Use postman to hit "/upload"  ->  "/files"  -> will show list of files you uploaded.
  
9. Build and run flask app in docker container locally (Ensure requirements.txt and dockerfile is there)
   docker desktop ->  running
   terminal -> app directory ->
   ```
   docker build -f docker-file/Dockerfile -t flask-app:latest .
   ```

10. Run container using above image
   ```
   docker run -p 5000:5000 -e FLASK_HOST=0.0.0.0 -e FLASK_PORT=5000 -e S3_BUCKET_NAME=s3-bucket-25-3def5b7f -e AWS_REGION=us-east-1 --name flask-app-container flask-app:v1
   ```
   - Containers MUST use 0.0.0.0  ->    127.0.0.1 works only on bare-metal, not in Docker.
  
   - -p 5000:5000 and FLASK_PORT=5000  ->  host port 5000 is mapped with container port 5000 and we are exposing port 5000 of flask app which is running inside container

     Request flows :  browser -> host port 5000 -> container port 5000 -> flask app port 5000
11. Now check browser ->  http://127.0.0.1/5000/health

12. App is working fine when we ran it as docker container locally. Now we will push app to github

13. Instance host  port   ->   container port    ->   flask port

    Note: container port and flask app port must match

    Note: Flask host decides which network interface it should listen on.
       127.0.0.1   ->   flask listens only inside container (used for local dev)
       0.0.0.0    ->    flask listens on all network interfaces, (Required for Docker, EC2)
14. Jenkinsfile
    ```
      docker.build(
             "flask-app:${env.BUILD_NUMBER}",
             "-f docker-file/Dockerfile ."
       )
    ```
    - uses jenkins pipeline groovy syntax instead of shell command ```  docker.build(<image_name>, <docker_build_args>)  ```
    - BUILD_NUMBER is automatically picked by jenkins. Jenkins assigns unique number to every pipeline run.
    - meaning : for every pipeline run, new image is created whose name is like 'flask-app:1' , 'flask-app:2' .... like this
   
    ```
      docker run -d --name flask-app-cont \
                      -e FLASK_HOST=${FLASK_HOST} \
                      -e FLASK_PORT=${FLASK_PORT} \
                      -e S3_BUCKET_NAME=${S3_BUCKET_NAME} \
                      -e AWS_REGION=${AWS_REGION} \
                      -p ${HOST_PORT}:${FLASK_PORT} \
                      flask-app:${env.BUILD_NUMBER}
    ```

    Here we don't want to hardcode env vars therefore we are using jenkins env vars.
    

13, We are done with writing Dockerfile, Jenkinsfile now

14. Install jenkins and docker on instance .

    ref  ->    https://github.com/OxSuyash/jenkins-notes/blob/main/install-jenkins.md
    ref  ->    https://github.com/OxSuyash/docker-notes/blob/main/install-docker.md

15. configure jenkins pipeline (Don't trigger build before step 16)  ->   https://github.com/OxSuyash/jenkins-notes/blob/main/workflow-jenkins-github.md

16. Configure env vars used in jenkinsfile

    manage jenkins  ->  system   ->   global properties   ->   environment variables

    Note: These are global properties. Each pipeline has access to it.  So, while creating env vars names, create app specific env var names, so they can be used separately for separate pipelins.

   Note: for jenkins file that will run app containers on ec2 instance we only need to give FLASK_HOST, FLASK_PORT, HOST_PORT, AWS_REGION, S3_BUCKET_NAME. Since we have attached IAM role to instance. 
   No need to give aws access keys and secret.

   FLASK_HOST   ->   which interface your flask app listening from (0.0.0.0  ->  all interface)
   FLASK_PORT   ->   which app port your app is listening on
   HOST_PORT    ->   which host port you have exposed on insatance
   AWS_REGION   ->   which region your instance is in
   S3_BUCKET_NAME  ->  which bucket your are connecting to 

17. Manual build jenkins pipeline  ->  from now on for every push to repo, pipeline gets triggered , new build will be generated.













