#!/bin/bash
# filepath: /home/aks/SPE Major/monitoring/entrypoint.sh
set -e

# Run initial scripts
python monitoring/model_registry.py  

# MLflow is already running in another container as per docker-compose
# No need to run: mlflow ui --host 0.0.0.0 --port 5000 &

# Run one-time scripts
python monitoring/retrain_model.py

# Set up periodic monitoring
while true; do
    echo "Running monitoring checks..."
    python monitoring/mlflow_tracking.py
    python monitoring/drift_detection.py
    echo "Monitoring complete. Sleeping for 1 hour..."
    sleep 3600*24*10  # Run monitoring every 10 days
done
