import json
import time
import threading
import duckdb
import random
import torch
import torch.nn as nn
import torch.optim as optim
from fastapi import FastAPI, WebSocket
from queue import Queue

# Initialize DuckDB for real-time message storage and analytics
duckdb_conn = duckdb.connect(database=':memory:')
duckdb_conn.execute("""
CREATE TABLE messages (
    message_id UUID DEFAULT gen_random_uuid(),
    message_type TEXT,
    payload JSON,
    priority FLOAT,
    event_time TIMESTAMP DEFAULT now()
);
""")

# Message Queue for Asynchronous Processing
message_queue = Queue()

# Define the Swarm Queen Model (Neural Network for Message Prioritization)
class SwarmQueen(nn.Module):
    def __init__(self):
        super(SwarmQueen, self).__init__()
        self.fc1 = nn.Linear(5, 16)  # Input: message features
        self.fc2 = nn.Linear(16, 8)
        self.fc3 = nn.Linear(8, 1)   # Output: priority score
        self.activation = nn.ReLU()
    
    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))  # Priority score between 0 and 1
        return x

# Initialize the Queen Model and Optimizer
queen_model = SwarmQueen()
optimizer = optim.Adam(queen_model.parameters(), lr=0.01)
criterion = nn.MSELoss()

# Function to assign priority using the Swarm Queen
def assign_priority(message):
    input_tensor = torch.tensor([
        message.get("urgency", 0),
        message.get("importance", 0),
        message.get("complexity", 0),
        message.get("expected_time", 0),
        random.random()  # Add slight randomness
    ], dtype=torch.float32)
    with torch.no_grad():
        priority = queen_model(input_tensor).item()
    return priority

# Function to process messages asynchronously
def process_messages():
    while True:
        if not message_queue.empty():
            message = message_queue.get()
            priority = assign_priority(message["payload"])
            duckdb_conn.execute("INSERT INTO messages (message_type, payload, priority) VALUES (?, ?, ?)", 
                                (message['type'], json.dumps(message['payload']), priority))
        time.sleep(0.1)  # Simulate slight processing delay

# Start message processing thread
threading.Thread(target=process_messages, daemon=True).start()

# FastAPI Server for Message Ingestion and Querying
app = FastAPI()

@app.post("/send_message")
def send_message(message_type: str, payload: dict):
    message_queue.put({"type": message_type, "payload": payload})
    return {"status": "Message queued"}

@app.get("/query_messages")
def query_messages():
    return duckdb_conn.execute("SELECT * FROM messages ORDER BY priority DESC LIMIT 100").fetchall()

@app.websocket("/live_messages")
async def websocket_messages(websocket: WebSocket):
    await websocket.accept()
    while True:
        messages = duckdb_conn.execute("SELECT * FROM messages ORDER BY priority DESC LIMIT 10").fetchall()
        await websocket.send_json(messages)
        time.sleep(2)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
