# Sentiment Analysis using MLOps Technologies

A comprehensive end-to-end sentiment analysis system built with modern MLOps principles, featuring continuous integration, continuous deployment, and automated model monitoring.

## Authors
- Abhishek Kumar Singh (MT2024006)
- Chinmay Tavrej (MT2024162)

## Project Overview

This project implements a sentiment analysis system that classifies text into positive, neutral, or negative sentiments. The system is built with a focus on MLOps practices including:

- Automated model training and evaluation
- Model version control and registry with MLflow
- Drift detection and automated retraining
- Containerization with Docker
- CI/CD pipeline with Jenkins
- REST API for model serving
- Interactive Streamlit dashboard for end users


### Components

1. **Data Processing Pipeline**
   - Raw data ingestion and validation
   - Text preprocessing (removing links, numbers, special characters)
   - Text normalization (lowercasing, stemming)
   - Class balancing for better model performance
   
2. **Model Training**
   - Feature extraction using TF-IDF vectorization
   - ExtraTrees Classifier for sentiment prediction
   - Model performance evaluation (accuracy, precision, recall, F1)
   
3. **Model Registry and Versioning**
   - MLflow for experiment tracking and model versioning
   - Automated model registration
   - Model metadata and artifact storage
   
4. **Model Serving**
   - FastAPI backend for real-time predictions
   - Database integration for storing prediction results
   - RESTful endpoints for client applications
   
5. **Monitoring & Maintenance**
   - Drift detection using Kolmogorov-Smirnov test
   - Automated model retraining when drift is detected
   - Performance monitoring and alerting
   
6. **UI/Dashboard**
   - Streamlit-based interactive dashboard
   - Real-time sentiment analysis visualization
   - Historical analysis and insights

## MLOps Pipeline

The MLOps pipeline implements the following workflow:

1. **Data Pipeline**
   - Data collection and storage in CSV format
   - Data preprocessing to clean and normalize text
   - Dataset validation and quality checks
   
2. **Model Development**
   - Feature engineering using TF-IDF vectorization
   - Model training with cross-validation
   - Hyperparameter optimization
   - Performance metrics tracking in MLflow
   
3. **Model Registry**
   - Versioned models stored in MLflow registry
   - Model metadata and metrics tracking
   - Input examples for model validation
   
4. **Deployment**
   - Containerized deployment with Docker
   - FastAPI backend for model serving
   - Streamlit frontend for user interface
   
5. **Monitoring & Maintenance**
   - Continuous monitoring for data drift
   - Automated retraining when needed
   - Performance tracking over time

## Jenkins CI/CD Pipeline

The project uses Jenkins for continuous integration and deployment with the following stages:

1. **Checkout Repository**
   - Fetch the latest code from version control

2. **Set Up Python**
   - Ensure Python environment is properly configured

3. **Build Docker Images**
   - Build containerized applications with Docker Compose
   - Create images for:
     - Sentiment analysis API
     - Monitoring service
     - Streamlit application
     - MLflow tracking server

4. **Push Docker Images**
   - Push built images to Docker Hub registry
   - Tag images with appropriate versions

5. **Local Deployment**
   - Deploy all services locally
   - Clean up existing containers if necessary
   - Start new containers with Docker Compose

6. **Notification**
   - Send email notifications on build success/failure

## Project Structure

```
├── api/                        # FastAPI implementation for model serving
│   ├── fast_main.py            # API endpoints definition
│   ├── predict.py              # Prediction logic
│   ├── database_api.py         # Database operations for API
│   └── Dockerfile              # Container configuration for API
├── ANALYSIS/                   # Exploratory data analysis notebooks  
├── cicd/                       # CI/CD related scripts
│   └── retrain_trigger.py      # Script to trigger model retraining
├── DATA/                       # Data storage
│   ├── data.csv                # Original dataset
│   ├── data_modified.csv       # Preprocessed dataset
│   └── mlflow_modified.csv     # Dataset for MLflow tracking
├── databases/                  # Database operations
│   ├── db_config.py            # Database configuration
│   ├── init_db.py              # Database initialization
│   └── sentiment.db            # SQLite database
├── model_making/               # Model building components
│   ├── model_trainig.py        # Model training script
│   ├── splitin_x_y.py          # Data splitting utilities
│   └── word_vec.py             # Text vectorization utilities
├── monitoring/                 # Model monitoring components
│   ├── drift_detection.py      # Data drift detection
│   ├── mlflow_tracking.py      # MLflow integration
│   ├── model_registry.py       # Model registry operations
│   └── retrain_model.py        # Model retraining logic
├── preprocess/                 # Text preprocessing utilities
│   ├── dropping_na.py          # Handling missing values
│   ├── labeling.py             # Sentiment labeling
│   ├── making_lowerCase.py     # Text normalization
│   └── ...                     # Other preprocessing steps
├── Save_model/                 # Saved model artifacts
│   ├── extra_trees.jbl         # Trained model
│   └── tf_vectorizer.jbl       # TF-IDF vectorizer
├── STEPS/                      # Pipeline steps
│   ├── data_reading.py         # Data loading utilities
│   ├── data_validation.py      # Data validation
│   └── pipeline_main.py        # Main pipeline orchestration
├── streamlit_app/              # User interface
│   ├── app.py                  # Streamlit application
│   └── Dockerfile              # Container configuration for UI
├── docker-compose.yml          # Main Docker Compose configuration
├── Jenkinsfile                 # Jenkins pipeline definition
└── README.md                   # This documentation file
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Jenkins (for CI/CD)

### Running Locally

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Start services using Docker Compose:
   ```bash
   docker compose up -d
   ```

3. Access the services:
   - Streamlit frontend: http://localhost:8501
   - FastAPI backend: http://localhost:8000
   - MLflow dashboard: http://localhost:5000

### Running with Jenkins

1. Ensure Jenkins is installed with necessary plugins
2. Create a new pipeline job using the Jenkinsfile
3. Configure build triggers as needed
4. Run the pipeline

## API Documentation

### Sentiment Analysis Endpoint

```
POST /predict/

Request Body:
{
    "text": "Your text for sentiment analysis"
}

Response:
{
    "text": "Your text for sentiment analysis",
    "sentiment": "positive" | "neutral" | "negative"
}
```

## Monitoring and Maintenance

The system includes automatic monitoring features:

- **Drift Detection**: Automatically detects when the distribution of sentiment predictions changes significantly from the training data
- **Performance Tracking**: Monitors accuracy, precision, recall, and F1 score
- **Automated Retraining**: Triggers model retraining when drift is detected or performance degrades
- **MLflow Dashboard**: Provides visualization of model metrics and performance over time

## Future Improvements

- Implement A/B testing framework for model comparison
- Add support for multiple languages
- Enhance the model with deep learning approaches
- Implement more advanced drift detection algorithms
- Add real-time streaming data support