import os
import sys
import time
import signal
import threading
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from predict import predict_sentiment
from database_api import save_text_to_db
from databases.update_csv import updated_csv
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

SENTIMENT_MAP = {1: "positive", 0: "neutral", 2: "negative"}
MODEL_PATH = 'Save_model/extra_trees.jbl'
VEC_PATH = 'Save_model/tf_vectorizer.jbl'
last_check_time = 0
last_model_time = 0
model_checker_running = False

async def background_model_check():
    """Background task that periodically checks for model updates"""
    global last_check_time, last_model_time, model_checker_running
    
    # Set flag so we don't start multiple checkers
    model_checker_running = True
    
    try:
        while True:
            try:
                current_time = time.time()
                
                # Check model files every 30 seconds
                if current_time - last_check_time >= 300:  
                    last_check_time = current_time
                    
                    # Check if model files exist and have been updated
                    if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
                        model_time = max(
                            os.path.getmtime(MODEL_PATH),
                            os.path.getmtime(VEC_PATH)
                        )
                        
                        # If model is newer than what we've loaded before
                        if model_time > last_model_time:
                            print(f"New model detected (modified at {time.ctime(model_time)}). Restarting server...")
                            last_model_time = model_time
                            
                            # Restart server after a short delay
                            restart_server()
                            break  # Exit the loop; the new process will start its own checker
            except Exception as e:
                print(f"Error in model checker: {e}")
            
            # Wait before next check
            await asyncio.sleep(5)
            
    except asyncio.CancelledError:
        print("Model checker task was cancelled")
    finally:
        model_checker_running = False

def restart_server():
    """Restart the FastAPI server by terminating the process"""
    # Give a moment to finish current requests
    threading.Timer(2.0, lambda: os.kill(os.getpid(), signal.SIGTERM)).start()
    print("Server restart scheduled...")

class SentimentRequest(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    text: str
    sentiment: str
    model_updated_at: str

@app.on_event("startup")
async def startup_prometheus():
    Instrumentator().instrument(app).expose(app)

@app.post("/predict/", response_model=SentimentResponse)
def predict(request: SentimentRequest):
    # No model check here - done in background
    
    sentiment = predict_sentiment(request.text)  
    sentiment_label = SENTIMENT_MAP.get(sentiment, "unknown")  
    
    save_text_to_db(request.text, sentiment_label)  
    updated_csv()
    
    # Get model update time for response
    try:
        if os.path.exists(MODEL_PATH):
            model_updated_at = time.ctime(os.path.getmtime(MODEL_PATH))
        else:
            model_updated_at = "unknown"
    except Exception as e:
        model_updated_at = f"error: {str(e)}"
    
    return SentimentResponse(
        text=request.text, 
        sentiment=sentiment_label,
        model_updated_at=model_updated_at
    )

@app.on_event("startup")
async def startup_event():
    """Start background tasks when application starts"""
    # Initialize the last_model_time at startup
    global last_model_time
    try:
        if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
            last_model_time = max(
                os.path.getmtime(MODEL_PATH),
                os.path.getmtime(VEC_PATH)
            )
            print(f"Initial model timestamp: {time.ctime(last_model_time)}")
    except Exception as e:
        print(f"Error getting initial model timestamp: {e}")
    
    # Start background model checking task
    asyncio.create_task(background_model_check())
    print("Background model checker started")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up when the application shuts down"""
    print("Shutting down API server")