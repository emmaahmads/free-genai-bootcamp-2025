#!/bin/bash

# Set variables
GITHUB_REPO="https://github.com/espeak-ng/espeak-ng.git"
REPO_NAME="espeak-ng"
DOCKER_HUB_USER="superumi"  # Change this to your Docker Hub username
IMAGE_NAME="espeak-malay"
TAG="latest"
WORKDIR=~/temp/
cd $WORKDIR

# Clone repo if not already present
if [ ! -d "$REPO_NAME" ]; then
    echo "Cloning espeak-ng repository..."
    git clone $GITHUB_REPO
else
    echo "espeak-ng repository already exists. Pulling latest changes..."
    cd $REPO_NAME && git pull && cd ..
fi

# Navigate into the repo
cd $REPO_NAME || exit 1

# Build the Docker image
echo "Building the Docker image..."
# Create a Dockerfile
cat <<EOF > Dockerfile
FROM debian:latest

# Install dependencies
RUN apt-get update && apt-get install -y \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set default command
ENTRYPOINT ["espeak-ng"]
EOF
docker build -t $IMAGE_NAME -f Dockerfile .

# Tag the image for Docker Hub
echo "Tagging the image..."
docker tag $IMAGE_NAME $DOCKER_HUB_USER/$IMAGE_NAME:$TAG

# Push to Docker Hub
echo "Pushing the image to Docker Hub..."
docker login
docker push $DOCKER_HUB_USER/$IMAGE_NAME:$TAG

echo "✅ Build and push completed successfully!"
