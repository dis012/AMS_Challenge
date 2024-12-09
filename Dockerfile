# Use an official PyTorch image with CUDA support as the base
FROM nvidia/cuda:11.8.0-devel-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH=/usr/local/cuda/bin:$PATH
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    git \
    wget \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3 as default
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Upgrade pip
RUN python -m pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /app

# Add the src directory to the Python path
ENV PYTHONPATH="/app/src:/app:$PYTHONPATH"

# Set the entry point
ENTRYPOINT ["python", "cli.py"]
