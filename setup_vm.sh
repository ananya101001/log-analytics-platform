#!/bin/bash

# --- Configuration ---
# Your project ID
export PROJECT_ID="graceful-trees-471716-s6"

# The name for your VM and static IP
export VM_NAME="data-services-vm"

# The region and zone to deploy to
export REGION="us-central1"
export ZONE="us-central1-c"

# --- Script Start ---
echo "--- Setting project to $PROJECT_ID ---"
gcloud config set project $PROJECT_ID

echo "--- Creating VM instance: $VM_NAME ---"
gcloud compute instances create $VM_NAME \
    --zone=$ZONE \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud

echo "--- Reserving a static IP address ---"
gcloud compute addresses create $VM_NAME-static-ip --region=$REGION
export STATIC_IP=$(gcloud compute addresses describe $VM_NAME-static-ip --region=$REGION --format="value(address)")
gcloud compute instances add-access-config $VM_NAME --zone=$ZONE --address=$STATIC_IP

echo "--- Creating firewall rule for Kafka (port 29092) ---"
gcloud compute firewall-rules create allow-kafka \
    --allow tcp:29092 \
    --source-ranges=0.0.0.0/0 \
    --description="Allow Kafka traffic"

echo "--- Creating firewall rule for ClickHouse (port 8123) ---"
gcloud compute firewall-rules create allow-clickhouse \
    --allow tcp:8123 \
    --source-ranges=0.0.0.0/0 \
    --description="Allow ClickHouse traffic"

echo "--- ✅ Setup Complete ---"
echo "Your Static IP is: $STATIC_IP"
echo "You can now SSH into the VM with: gcloud compute ssh $VM_NAME --zone=$ZONE"