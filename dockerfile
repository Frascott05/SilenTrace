FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# Imposta directory
WORKDIR /app

# Clona Volatility
RUN git clone https://github.com/Frascott05/volatility3 /opt/volatility3

# Copia requirements
COPY requirements.txt .

# Installa dipendenze
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copia il progetto Flask
COPY . .

# Espone porta Flask
EXPOSE 5000

# Avvio app
CMD ["/bin/bash"]
#CMD ["flask", "run"]