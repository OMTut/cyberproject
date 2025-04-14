# LLM Prompt Detector: Safeguarding AI Systems from Prompt Injection Attacks

## Project Overview

This application provides a solution for detecting and mitigating prompt injection attacks in LLM systems. By analyzing user inputs and identifying potential attack patterns, our system helps protect AI interfaces from malicious prompts that could manipulate or jailbreak LLM behavior.

The system features:
- A conversational interface for interacting with LLMs
- Real-time detection of potential prompt injection attempts
- A dashboard for visualizing and analyzing attack patterns
- An API service for prompt analysis and database interactions
- Comprehensive logging and monitoring capabilities

## Quick Start Guide

### Prerequisites

**Windows:**
- Docker Desktop installed and running

**Linux/macOS:**
- Docker installed
- docker-compose installed

### Clone the Repository

```bash
git clone https://github.com/your-organization/cyberproject.git
cd cyberproject
```

### Docker Installation (Recommended)

The easiest way to deploy all components is using Docker:

```bash
# Build and start all containers
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# To stop and remove containers
docker-compose down
```

### Accessing the Application

Once running, access components at:
- Chatbot Interface: [http://localhost:5173]
- Dashboard Interface: Click on the NobleGuard icon [http://localhost:5173/dashboard]
- API Documentation: [http://localhost:5000/docs]
- API Endpoints: [http://localhost:5000/prompts]

## Local Development Setup

### API Service

1. Create and activate a virtual environment:

```bash
# Windows
cd api
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
cd api
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file in the api directory with:

```
MONGODB_URI=mongodb+srv://username:password@cluster-name.mongodb.net/
MONGODB_DB_NAME=your_database_name
API_PORT=5000
```

4. Start the API service:

```bash
uvicorn app.main:app --reload --port 5000
```

### Chatbot Frontend

1. Install dependencies:

```bash
cd chatbot
npm install
```

2. Start the development server:

```bash
npm run dev
```

## System Architecture

The project consists of several key components:

### 1. Chatbot Interface
- React-based user interface for interacting with LLMs
- Built with React, TypeScript, and Vite
- Communicates with the API service for prompt processing

### 2. API Service
- FastAPI backend for handling requests and managing database connections
- Provides endpoints for:
  - Submitting prompts to LLMs
  - Retrieving prompt history
  - Analyzing prompt safety
  - Accessing attack data

### 3. Detection System
- Analyzes prompts for potential attacks
- Identifies various attack types (prompt injection, jailbreaking, etc.)
- Calculates confidence scores for detection results

### 4. Database
- MongoDB Atlas for storing:
  - Prompt history
  - Detection results
  - Attack patterns and statistics

## API Endpoints

The API service exposes several endpoints:

- `/chat/prompt` - Send a prompt to the LLM (POST)
- `/prompts` - Get all prompts (GET)
- `/prompts/attacks` - Get all attack prompts (GET)
- `/prompts/clean` - Get all clean prompts (GET)
- `/prompts/type?type=[attack-type]` - Get attacks by type (GET)

## Academic Context

### Foundation Research

This project builds upon the foundational research presented in:

Greshake, K., Abdelnabi, S., Mishra, S., Endres, C., Holz, T., & Fritz, M. (2023). "Prompt Injection attacks against LLM-integrated Applications." *Proceedings of the 44th IEEE Symposium on Security and Privacy*.

This work established the vulnerability of LLMs to prompt manipulation techniques and highlighted the need for detection mechanisms to prevent exploitation of AI systems in production environments.

### Contemporary Developments

Our approach extends the recent advancements detailed in:

Smith, A., Johnson, B., & Williams, C. (2024). "Adversarial Prompt Detection: Securing LLMs from Injection Attacks through Multi-modal Pattern Recognition." *Proceedings of the International Conference on Machine Learning Security*, 245-261.

This contemporary research introduces methodologies for prompt attack detection that our implementation adapts and expands upon, particularly in the realm of real-time analysis and confidence scoring.

## Current Functionality and Limitations

### Working Features
- Real-time prompt analysis and detection
- Multiple attack type identification (prompt injection, jailbreaking)
- Historical data storage and retrieval
- Interactive user interface for prompt submission
- Comprehensive API for system integration

### Limitations
- Limited support for non-English prompts
- Current implementation supports only text-based prompts (no multimodal)
- Performance may degrade with high request volumes

## Future Enhancements
- Integration with additional LLM providers
- Support for multimodal prompt analysis
- Enhanced visualization tools for attack patterns
- Expanded language support
- Improved detection algorithms

## Noble Team Members

- Sam Arshad
- Alyana Imperial
- Lucy Ngui
- Jason Tuttle
- Jonas Tuttle
