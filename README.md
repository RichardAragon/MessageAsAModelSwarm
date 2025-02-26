# Messages-as-Models: Swarm Queen Optimization

## Overview
The **Messages-as-Models** prototype implements an **AI-driven execution framework**, where messages are treated as **first-class data models** and dynamically prioritized by a **Swarm Queen AI model**. This system enables **real-time message processing**, prioritization, and execution optimization in an event-driven architecture.

## Key Features
- **Swarm Queen AI Model**: Uses a neural network to **assign priority** to incoming messages.
- **DuckDB Storage**: Efficiently stores and queries messages in real-time.
- **FastAPI REST API**: Provides endpoints for **sending and querying messages**.
- **WebSocket Live Streaming**: Streams **top-priority messages in real-time**.
- **Asynchronous Processing**: Messages are **queued and processed dynamically**.

## Architecture
### 1. **Message Ingestion**
- Messages are sent via a REST API (`/send_message`).
- Each message contains **metadata** such as urgency, importance, and complexity.

### 2. **Swarm Queen AI Model**
- A **neural network** evaluates the message and **assigns a priority score**.
- Scores are based on **urgency, importance, complexity, expected execution time**, and **random variation**.

### 3. **Storage and Querying**
- Messages are stored in **DuckDB** for fast analytics.
- Users can query messages by priority via `/query_messages`.

### 4. **Live Execution Monitoring**
- **WebSocket API (`/live_messages`)** streams messages dynamically based on priority.

## Installation
### Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **Pip**

### Install Dependencies
```sh
pip install fastapi uvicorn duckdb torch
```

### Running the Application
```sh
python messages_as_models.py
```
The FastAPI server will start on `http://localhost:8000`.

## API Endpoints
### 1. **Send a Message**
```sh
POST /send_message
```
#### **Request Body**
```json
{
  "message_type": "task",
  "payload": {
    "urgency": 0.9,
    "importance": 0.8,
    "complexity": 0.5,
    "expected_time": 0.3
  }
}
```
#### **Response**
```json
{
  "status": "Message queued"
}
```

### 2. **Query Stored Messages**
```sh
GET /query_messages
```
#### **Response Example**
```json
[
  {
    "message_id": "a1b2c3",
    "message_type": "task",
    "payload": "{...}",
    "priority": 0.92,
    "event_time": "2025-02-26 12:00:00"
  }
]
```

### 3. **Live Streaming Messages**
```sh
WebSocket /live_messages
```
- Connect via WebSocket to receive **live, high-priority messages**.

## Future Enhancements
- **Reinforcement Learning**: Enable adaptive learning to improve priority assignment.
- **Distributed Worker Agents**: Implement worker agents that act on prioritized messages.
- **Optimized Execution Models**: Improve AI-driven decision-making using self-organizing strategies.

## Contributing
- Fork the repository.
- Submit pull requests with clear explanations.
- Join discussions on improving the model and execution logic.

## License
This project is **open-source** under the MIT License.

