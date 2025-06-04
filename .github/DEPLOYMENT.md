# Deployment Guide

This project is configured to automatically deploy to your SSH server using GitHub Actions.

## Prerequisites

- A server with SSH access
- Docker and Docker Compose installed on the server
- Git repository access on the server

## Setting Up GitHub Secrets

You need to set up the following secrets in your GitHub repository:

1. `SSH_PRIVATE_KEY`: Your private SSH key
   - Generate a new key pair if needed: `ssh-keygen -t ed25519 -f ~/.ssh/github_deploy`
   - Add the public key to your server's `~/.ssh/authorized_keys`
   - Copy the entire private key including header/footer: `cat ~/.ssh/github_deploy`

2. `SSH_KNOWN_HOSTS`: Your server's SSH fingerprint
   - Get this by running: `ssh-keyscan -t rsa your-server-hostname`

3. `SSH_USER`: Your username on the SSH server

4. `SSH_HOST`: Your server's hostname or IP address

5. `PROJECT_PATH`: The absolute path to your project on the server

## Manual Deployment

If you need to deploy manually:

```bash
# SSH into your server
ssh your-username@your-server

# Navigate to your project directory
cd /path/to/project

# Pull the latest changes
git pull

# Restart the Docker containers
docker-compose -f prod.yml down
docker-compose -f prod.yml up -d --build
``` 