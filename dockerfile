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

# Setting the working directory
WORKDIR /app

# Clone Volatility
RUN git clone https://github.com/Frascott05/volatility3 /opt/volatility3

# requirements copy
COPY requirements.txt .

# Install dependeces
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy flask project
COPY . .

# Expose Flask port
EXPOSE 5000

#CMD ["/bin/bash"]
CMD ["flask", "run"]