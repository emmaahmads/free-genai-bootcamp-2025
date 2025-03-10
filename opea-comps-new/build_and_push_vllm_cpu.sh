#!/bin/bash

# Set variables
GITHUB_REPO="https://github.com/vllm-project/vllm.git"
REPO_NAME="vllm"
DOCKER_HUB_USER="superumi"  # Change this to your Docker Hub username
IMAGE_NAME="vllm-cpu"
TAG="latest"

# Clone repo if not already present
if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning vLLM repository..."
    git clone $GITHUB_REPO
else
    echo "vLLM repository already exists. Pulling latest changes..."
    cd $REPO_NAME && git pull && cd ..
fi

# Navigate into the repo
cd $REPO_NAME || exit 1

# Build the Docker image
echo "Building the Docker image..."
docker build -t $IMAGE_NAME -f Dockerfile.cpu .

# Tag the image for Docker Hub
echo "Tagging the image..."
docker tag $IMAGE_NAME $DOCKER_HUB_USER/$IMAGE_NAME:$TAG

# Push to Docker Hub
echo "Pushing the image to Docker Hub..."
docker login
docker push $DOCKER_HUB_USER/$IMAGE_NAME:$TAG

echo "✅ Build and push completed successfully!"
