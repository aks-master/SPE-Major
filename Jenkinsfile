pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = 'sentiment_repo_cicd' // Replace with your image name
    }

    stages {
        stage('Checkout Repository') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python') {
            steps {
                script {
                    def pythonInstalled = sh(script: 'python --version', returnStatus: true)
                    if (pythonInstalled != 0) {
                        error("Python is not installed or not available in the PATH. Build failed.")
                    }
                }
            }
        }

        stage('Build Docker Images Using Docker Compose') {
            steps {
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('', 'DockerHubCred') {
                        // Tag and push the sentiment API image
                        sh "docker tag ${DOCKER_IMAGE_NAME}/sentiment_api aks00798/${DOCKER_IMAGE_NAME}_sentiment_api:latest"
                        sh "docker push aks00798/${DOCKER_IMAGE_NAME}_sentiment_api"

                        // Tag and push the monitoring service image
                        sh "docker tag ${DOCKER_IMAGE_NAME}/monitoring_service aks00798/${DOCKER_IMAGE_NAME}_monitoring_service:latest"
                        sh "docker push aks00798/${DOCKER_IMAGE_NAME}_monitoring_service"

                        // Tag and push the Streamlit app image
                        sh "docker tag ${DOCKER_IMAGE_NAME}/streamlit_app aks00798/${DOCKER_IMAGE_NAME}_streamlit_app:latest"
                        sh "docker push aks00798/${DOCKER_IMAGE_NAME}_streamlit_app"
                    }
                }
            }
        }

        stage('Local Deployment') {
            steps {
                sh '''
                    echo "🚀 Pulling Docker Images for Local Deployment..."
                    docker pull aks00798/${DOCKER_IMAGE_NAME}_sentiment_api:latest
                    docker pull aks00798/${DOCKER_IMAGE_NAME}_monitoring_service:latest
                    docker pull aks00798/${DOCKER_IMAGE_NAME}_streamlit_app:latest

                    echo "🔧 Starting Docker Compose for Local Deployment..."
                    docker compose up -d

                    echo "🎉 Deployment Complete!"
                    echo "🖥️  Backend API accessible at: http://localhost:8000"
                    echo "🌐 Frontend (Streamlit) accessible at: http://localhost:8501"
                    echo "📊 MLflow Dashboard accessible at: http://localhost:5000"
                '''
            }
        }
    }
}