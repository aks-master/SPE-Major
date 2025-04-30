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
            environment {
                KUBECONFIG = credentials('kubernetes-config')
            }
            steps {
                sh '''
                    echo "🚀 Pulling Docker Images for Local Deployment..."
                    docker pull ${DOCKER_IMAGE_NAME_PREFIX}_sentiment_api:latest
                    docker pull ${DOCKER_IMAGE_NAME_PREFIX}_monitoring_service:latest
                    docker pull ${DOCKER_IMAGE_NAME_PREFIX}_streamlit_app:latest

                    # Check and remove conflicting containers
                    docker ps -a | grep mlflow_tracking && docker stop mlflow_tracking && docker rm mlflow_tracking || echo "No existing mlflow_tracking container to remove."
                    docker ps -a | grep monitoring_service && docker stop monitoring_service && docker rm monitoring_service || echo "No existing monitoring_service container to remove."
                    docker ps -a | grep streamlit_app && docker stop streamlit_app && docker rm streamlit_app || echo "No existing streamlit_app container to remove."
                    docker ps -a | grep sentiment_api && docker stop sentiment_api && docker rm sentiment_api || echo "No existing sentiment_api container to remove."

                    # Debug information about kubeconfig
                    echo "KUBECONFIG value: $KUBECONFIG"
                    # ls -la $KUBECONFIG
                    
                    # Debug: Check if kubeconfig is valid
                    kubectl config view
                    
                    # Apply the manifests in order
                    kubectl apply -f k8s/01-namespace.yaml
                    kubectl apply -f k8s/02-configmap.yaml
                    kubectl apply -f k8s/03-persistent-volume.yaml
                    kubectl apply -f k8s/04-mlflow-deployment.yaml
                    kubectl apply -f k8s/05-monitoring-deployment.yaml
                    kubectl apply -f k8s/06-backend-deployment.yaml
                    kubectl apply -f k8s/07-frontend-deployment.yaml
                    kubectl apply -f k8s/08-prometheus.yaml
                    kubectl apply -f k8s/09-grafana.yaml
                    kubectl apply -f k8s/10-ingress.yaml
                    
                    # Verify deployments
                    kubectl get pods -n sentiment-analysis
                '''
            }
        }
    }

    post {
        success {
            mail to: 'amit33301@gmail.com', 
                 subject: "✅ Build Successful: SPE Major Project",
                 body: "Build ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded.\nLogs: ${env.BUILD_URL}"
        }

        failure {
            mail to: 'amit33301@gmail.com', 
                 subject: "❌ Build Failed: SPE Major Project",
                 body: "Build ${env.JOB_NAME} #${env.BUILD_NUMBER} failed.\nLogs: ${env.BUILD_URL}"
        }
    }
}
// Note: Ensure that the DockerHubCred and kubernetes-config credentials are set up in Jenkins.
// Note: The Docker image names and tags should be adjusted according to your naming conventions.
