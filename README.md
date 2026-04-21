# Volatility Plugin API

API for Volatility plugin execution on a memory dump , async job management and results recovery.

---

## 📌 Overview

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
