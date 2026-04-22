
# SilenTrace 2.0
![SilentTrace Logo](DocumentationLogo.jpeg)


API for Volatility plugin execution on a memory dump , async job management and results recovery.
Backend API are made in python, using FastAPI, meanwhile the frontend (that can be changed with your own personal frontend)
was created with REACT.

---
# Starting the project:

## Necessary:

Install all the requirements for python with the following command:
```bash
pip install -r requirements.txt
```
And the dependencies for React (see below).

Before starting the project is essential to create a folder named `dumps`
(or whatever name you like), that will contain all the dumps that you want to analyze.

In addition to that, you have to create the `.env` file, that has to be something like this:

```bash
APP_NAME=SilentraceGUI

VOLATILITY_PATH=/complete/path/to/volatility/vol.py
DUMPS_PATH=/complete/path/to/dumps/folder

ALLOWED_ORIGINS=*
PORT_BACKEND=9000 #do not change that unless you kwnow ho to deal with react
```

## Starting with one command (LINUX only):

```bash
./start.sh
```
if it doesn't start cause it doesn't have permission, run this command:

```bash
chmod +x start.sh
```
and now re-run again the first command.

## Starting the project on another OS (Docker required):

⚠️ You don't have to clone the git repository of the project, you just have to create a folder with the `.env` file, the `dumps` folder
and the following `dockerfile` and `docker-compose.yml`.

###dockerfile
```dockerfile
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    gcc \
    make \
    python3-dev \
    libffi-dev \
    libssl-dev \
    rustc \
    cargo \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel

# ----------------------------
# VOLATILITY3 in /opt
# ----------------------------
RUN git clone https://github.com/Frascott05/volatility3 /opt/volatility3

#ENV PYTHONPATH="/opt/volatility3"

# ----------------------------
# PROGETTO SILENTRACE in /home/app
# ----------------------------
WORKDIR /home/app

RUN git clone -b SilenTrace-2.0 https://github.com/Frascott05/SilenTrace.git

WORKDIR /home/app/SilenTrace

# ----------------------------
# BACKEND dependencies
# ----------------------------
RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------
# FRONTEND dependencies
# ----------------------------
#RUN cd frontend && npm install

# ----------------------------
# start script permissions
# ----------------------------
RUN chmod +x /home/app/SilenTrace/start.sh

# Porta React
EXPOSE 5173

# Porta FastAPI
EXPOSE 9000

# Avvio
CMD ["/home/app/SilenTrace/start.sh"]

```
### docker-compose.yml
```docker-compose.yml
version: "3.9"

services:
  silentrace:
    build: .

    container_name: silentrace

    ports:
      - "5173:5173"
      - "9000:9000"

    volumes:
      # dati persistenti
      - ./dumps:/home/app/SilenTrace/dumps

      # env esterno
      - ./.env:/home/app/SilenTrace/.env

    working_dir: /home/app/SilenTrace

    stdin_open: true
    tty: true
```

---

## 📌 Overview of the backend API

Those API allows to:

- Start an analysis on a specified dump file
- Monitoring the status of the asyncronous jobs
- Retrieving the results of the analysis
- Getting the specified OS avaible plugins
- Starting a parsing pipeline for a timeline

---

## 🧠 Job States

The possible states are:

- `running`
- `done`

---

## 🧾 Models

### RunRequest

```python
class RunRequest(BaseModel):
    memory_file: str
    plugins: List[str]
    os: Optional[str] = "windows"
    address: Optional[str] = None
    dump: Optional[bool] = False
    process: Optional[int] = None
```

---

### ListRequest

```python
class ListRequest(BaseModel):
    os: Optional[str] = "windows"
```

---

### TimelineRequest

```python
class TimelineRequest(BaseModel):
    memory_file: str
    os: Optional[str] = "windows"
```

---

## 🚀 Endpoints

---

### POST /run

Starting the execution of Volatility plugin on a memory dump.

**Request body:**

```json
{
  "memory_file": "/path/to/memory.dmp",
  "plugins": ["pslist", "netscan"],
  "os": "windows",
  "address": null,
  "dump": false,
  "process": null
}
```

**Response:**

```json
{
  "job_id": "abc123"
}
```

---

### GET /status/{job_id}

Job results state.

**Response:**

```json
{
  "job_id": "abc123",
  "status": "running | done"
}
```

---

### GET /results/{job_id}

Getting analysis result.

**Response:**

```json
{
  "results": {
    "pslist": [
      {
        "pid": 1234,
        "name": "explorer.exe"
      }
    ]
  }
}
```

---

### POST /plugin-list

Gaining the plugin list avaible for the operative system.

**Request:**

```json
{
  "os": "windows"
}
```

**Response:**

```json
{
  "plugins": ["pslist", "netscan", "malfind"]
}
```

---

### POST /timeline

Starts the parsing for the timeline on a memory dump (windows only for now).

**Request:**

```json
{
  "memory_file": "/path/to/memory.dmp",
  "os": "windows"
}
```

**Response:**

```json
{
  "job_id": "abc123"
}
```

---

## 🔄 Workflow

1. `/plugin-list`
2. `/run` o `/timeline`
3. `/status/{job_id}`
4. `/results/{job_id}`

---

## ▶️ Server started

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```


# Frontend Documentation

## Prerequisites

Before starting, make sure you have installed:

- Node.js (>= 18)
- npm (comes with Node.js)
- Python 3.10+ (only if backend dependencies are required)

---

## Installation

### 1. Install Node.js

Inside the frontend project folder:

```bash
npm install
```
This will install all the necessaries dependencies for the project




