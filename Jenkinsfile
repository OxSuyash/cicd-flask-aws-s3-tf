pipeline {
    agent any

    environment {
        // App-level configuration (used INSIDE container)
        FLASK_HOST     = "${env.FLASK_HOST}"
        FLASK_PORT     = "${env.FLASK_PORT}"
        S3_BUCKET_NAME = "${env.S3_BUCKET_NAME}"
        AWS_REGION     = "${env.AWS_REGION}"

        // Infra-level configuration (used by Docker only)
        HOST_PORT      = "${env.HOST_PORT}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(
                        "flask-app:${env.BUILD_NUMBER}",
                        "-f docker-file/Dockerfile ."
                    )
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python -m pytest tests/ -v'
            }
        }

        stage('Deploy Container') {
            steps {
                script {
                    // Stop and remove old container if exists
                    sh 'docker rm -f flask-app-cont || true'

                    // Run new container
                    sh """
                    docker run -d --name flask-app-cont \
                      -e FLASK_HOST=${FLASK_HOST} \
                      -e FLASK_PORT=${FLASK_PORT} \
                      -e S3_BUCKET_NAME=${S3_BUCKET_NAME} \
                      -e AWS_REGION=${AWS_REGION} \
                      -p ${HOST_PORT}:${FLASK_PORT} \
                      flask-app:${env.BUILD_NUMBER}
                    """
                }
            }
        }
    }

    post {
        success {
            echo "Deployment successful"
        }
        failure {
            echo "Pipeline failed"
        }
    }
}
