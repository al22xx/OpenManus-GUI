#!/bin/bash

# Stop and remove any existing container
docker rm -f openmanus-container 2>/dev/null

# Build the Docker image
docker build -t openmanus .

# Run with ALL environment variables from .env
docker run -d -p 7860:7860 \
  -v $(pwd)/.env:/workspace/.env \
  --env-file .env \
  --name openmanus-container \
  openmanus

# Show startup logs
echo -e "\n🔄 Container starting... (wait 10 seconds)"
sleep 10
docker logs openmanus-container

# Display access URL
echo -e "\n✅ Ready! Access at: http://localhost:7860"