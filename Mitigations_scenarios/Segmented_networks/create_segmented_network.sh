#!/bin/bash
# create_segmented_network.sh

echo "Creating Purdue Model Network Segmentation..."

# Create subnet networks
echo "Creating subnets..."

# Field Device Network (Level 0-1)
docker network create --driver=bridge --subnet=172.18.1.0/24 --gateway=172.18.1.1 field_device

# Supervisory Network (Level 2)  
docker network create --driver=bridge --subnet=172.18.2.0/24 --gateway=172.18.2.1 supervisory

# DMZ Network (Level 3)
docker network create --driver=bridge  --subnet=172.18.3.0/24 --gateway=172.18.3.1  dmz

# Corporate Network (Level 4-5)
docker network create  --driver=bridge --subnet=172.18.4.0/24  --gateway=172.18.4.1 corporate

echo "Networks created successfully!"
docker network ls | grep -E "(field_device|supervisory|dmz|corporate)"
