from flask import Flask
from scheduler.job_scheduler import run_scheduler
import threading
from typing import List

app = Flask(__name__)

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

def start_scheduler(tokens: List[str]):
    run_scheduler(tokens)  # Or asyncio.run(run_scheduler()) if it's an async function

if __name__ == "__main__":
    tokens = ["BTCUSDT", "SOLUSDT"]
    # Run the scheduler in a separate thread
    threading.Thread(target=run_scheduler, args=(tokens, ), daemon=True).start()

    # Start the Flask app
    app.run(host="0.0.0.0", port=8000)