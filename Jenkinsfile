pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME_PREFIX = 'aks00798/sentiment_repo_cicd' // Prefix for Docker images
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
                    // Check if Python is installed; install it if missing
                    def pythonInstalled = sh(script: 'command -v python3', returnStatus: true)
                    if (pythonInstalled != 0) {
                        echo "Python is not installed. Installing Python..."
                        sh '''
                            sudo apt-get update
                            sudo apt-get install -y python3 python3-pip
                        '''
                    } else {
                        echo "Python is already installed."
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
                        sh "docker tag ${DOCKER_IMAGE_NAME_PREFIX}/sentiment_api ${DOCKER_IMAGE_NAME_PREFIX}_sentiment_api:latest"
                        sh "docker push ${DOCKER_IMAGE_NAME_PREFIX}_sentiment_api:latest"

                        // Tag and push the monitoring service image
                        sh "docker tag ${DOCKER_IMAGE_NAME_PREFIX}/monitoring_service ${DOCKER_IMAGE_NAME_PREFIX}_monitoring_service:latest"
                        sh "docker push ${DOCKER_IMAGE_NAME_PREFIX}_monitoring_service:latest"

                        // Tag and push the Streamlit app image
                        sh "docker tag ${DOCKER_IMAGE_NAME_PREFIX}/streamlit_app ${DOCKER_IMAGE_NAME_PREFIX}_streamlit_app:latest"
                        sh "docker push ${DOCKER_IMAGE_NAME_PREFIX}_streamlit_app:latest"
                    }
                }
            }
        }

        stage('Local Deployment') {
            steps {
                sh '''
                    echo "🚀 Pulling Docker Images for Local Deployment..."
                    docker pull ${DOCKER_IMAGE_NAME_PREFIX}_sentiment_api:latest
                    docker pull ${DOCKER_IMAGE_NAME_PREFIX}_monitoring_service:latest
                    docker pull ${DOCKER_IMAGE_NAME_PREFIX}_streamlit_app:latest

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