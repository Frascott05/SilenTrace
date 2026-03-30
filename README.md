# SilentTrace
![SilentTrace Logo](DocumentationLogo.jpeg)

SilentTrace is a **Flask-based memory forensics web application** designed to analyze memory dumps using **Volatility 3**.  
It provides a simple UI to manage investigations and execute analysis plugins on uploaded memory dumps.

---

## ⚠️ Security Notice

> 🚫 **DO NOT deploy this application on the public internet**

This project is designed **only for local usage**:

- Personal machine
- Local lab environment
- Internal server (LAN)

Even though JWT authentication is implemented, this release:

- Is **not hardened for production**
- Does **not include advanced security protections**
- May expose sensitive forensic data

👉 Use it only in **controlled environments**

---

## 📁 Project Structure

- `app/` → Flask application
- `dumps/` → Memory dumps folder (mounted inside container)
- `Volatility*Runner.py` → Core logic for running Volatility
- `docker-compose.yml` → Container orchestration
- `Dockerfile` → Container build instructions
- `.env` → Environment configuration

---

## ⚙️ Configuration (.env)

### 🔐 Important Settings

#### 1. SECRET_KEY (CRITICAL)

```env
SECRET_KEY="your-secret-key"
```

- Used for JWT authentication
- **MUST be changed before usage**
- Never expose it publicly

---

#### 2. JWT Expiration

```env
JWT_EXPIRATION_HOURS=24
```

Controls how long tokens remain valid.

---

#### 3. Volatility Path

```env
VOLATILITY_PATH="/opt/volatility3/vol.py"
```

- Path to Volatility inside the container
- Change it only if you modify the Dockerfile
- We strongly reccomend to not change this or else you'll have to change also part of the code

---

#### 4. Dumps Path (VERY IMPORTANT)

```env
PATH_TO_MOUT="dumps"
```

This defines the folder mounted inside the container

👉 You can:

- Use a local folder (`dumps`)
- Use an external drive:
    
```env
PATH_TO_MOUT="/media/external_drive/memory_dumps"
```
    
This allows:

- Persistent storage
- Large dump handling
- External forensic datasets

---

#### 5. Port Configuration

```docker
PORT=5000
```

You can change it freely:

```docker
PORT=8080
```

---

#### 6. Debug Mode

`DEBUG=True`

```Set to `False` in more stable environments```

---

## 🧩 Customizing Volatility Plugins

Plugins are defined in:

```
app/services/enums/VolatilityPlugins.py
```

### Default Example:

```python
class VolatilityPlugins(Enum):  
    PSTREE = "pstree"  
    NETSCAN = "netscan"  
    HASHDUMP = "hashdump"  
    PSXVIEW = "psxview"

```

---

### ➕ Adding a New Plugin

Example: adding a shutdown registry plugin
```python
class VolatilityPlugins(Enum):  
    PSTREE = "pstree"  #DO NOT REMOVE
    NETSCAN = "netscan"  
    HASHDUMP = "hashdump"  
    PSXVIEW = "psxview"  
    SHUTDOWN = "registry.shutdown"

```

NOTE: the more plugins you add, more is the time to wait before the complete execution of them all. We strongly suggest you to only set the plugins that you need and remove the others (exept for pstree).

---

### 📌 Notes

- The value must match the Volatility plugin name
- Format:
    - With OS: `windows.pslist`
    - Without OS: `pslist`

The system automatically builds commands like:

python3 vol.py -f dump windows.pstree

---

## 💻 Customizing Default Operating System

Defined in:

```
app/services/enums/OperativeSystem.py
```

### Default:
```python
class OperativeSystems(Enum):  
    WINDOWS = "windows"  
    MAC_OS = "mac"  
    LINUX = "linux"  
    DEFAULT = WINDOWS
```

---

### 🔧 Changing Default OS

Example: set Linux as default

```python
DEFAULT = LINUX
```

---

## 🐳 Docker Usage

### 🔨 Build the Image
```bash
docker compose build
```

---

### 🚀 Run the Application

```bash
docker compose run --service-ports silentrace
```
This will:

- Start the Flask server
- Expose the configured port

---

### 🌐 Access the App

Open your browser:

http://localhost:5000

(or your configured port)

---
### 📂 Managing Dumps (Updated)

You can:
#### 1. Place dumps before startup

dumps/  
 ├── memory1.vmem  
 ├── memory2.raw

---

#### 2. Add dumps in real time (Recommended ✅)

Since the folder is mounted as a Docker volume:

```bash
/${PATH_TO_MOUT}:/app/app/static/uploads
```

👉 You can **add dumps while the container is running** by simply:

- Dragging files into the configured folder (e.g. `dumps/`)
- Copying files into that directory

✔ No container restart required  
✔ Files are immediately available inside the application

---
#### 3. Alternative (manual copy)

```bash
docker cp file.vmem silentrace:/app/app/static/uploads/
```


---

## 🧪 Development Mode

You can modify:

\#CMD ["flask", "run"]  
CMD ["/bin/bash"]

Then:

docker compose run --service-ports silentrace

And manually start:

```bash
flask run
```