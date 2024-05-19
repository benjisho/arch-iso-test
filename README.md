# Arch ISO Test

This repository contains the necessary configuration files and scripts to automate the build process of an Arch Linux ISO using Packer and Jenkins.

## Overview

The setup includes:
- A Packer template (`arch-iso.json`) to build a custom Arch Linux ISO.
- A Jenkins pipeline (`Jenkinsfile`) to automate the Packer build process.
- Scripts to handle dynamic SSH key generation and ISO checksum fetching.

## Prerequisites

- A Jenkins server with the following plugins:
  - Git Plugin
  - SSH Agent Plugin
- A Packer VM with the following installed:
  - Packer
  - QEMU
  - Git
  - Python

## Getting Started

### Setting Up the Packer VM

1. **Install Required Software:**
   ```bash
   sudo apt update
   sudo apt install packer qemu git python3 -y
   ```

2. **Ensure SSH Key Pair Exists:**
   Generate an SSH key pair if it does not already exist:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ```

3. **Clone the Repository:**
   ```bash
   git clone https://github.com/benjisho/arch-iso-test.git /opt/packer
   ```

### Jenkins Configuration

1. **Add SSH Key to Jenkins:**
   Add the SSH private key used for accessing the Packer VM to Jenkins credentials (Manage Jenkins -> Manage Credentials).

2. **Configure Jenkins Pipeline:**
   Ensure your Jenkins pipeline is set up to use the provided `Jenkinsfile`.

### Packer Template

The `arch-iso.json` template defines the build configuration for Packer. Key features include:
- Dynamic output directory creation.
- SSH setup for the live CD.
- Provisioning steps to install necessary software and run the custom install script.

### Fetch Checksum Script

The `fetch_checksum.sh` script fetches the latest checksum for the Arch Linux ISO.

### Jenkinsfile

The `Jenkinsfile` automates the build process with the following stages:
1. **Checkout:** Clones the repository.
2. **Build Image:** Runs the Packer build process, dynamically generating SSH keys and fetching the ISO checksum.
3. **Copy ISO:** Copies the generated ISO file to the Jenkins workspace.
4. **Shutdown VM:** Shuts down the Packer VM after the build.

### Running the Build

Trigger the Jenkins job to start the build process. The pipeline will:
1. Clone the repository.
2. Generate a unique output directory for the ISO.
3. Fetch the latest ISO checksum.
4. Run the Packer build.
5. Copy the generated ISO to the Jenkins workspace.
6. Shut down the Packer VM.

### Post-Build Actions

- **Success:** Archives the ISO file locally on Jenkins.
- **Failure:** Captures and prints the error log, archiving any log files for further investigation.

## Example Usage

1. **Trigger the Jenkins Job:**
   Start the Jenkins job to initiate the build process.

2. **Monitor the Build:**
   Monitor the Jenkins console output for build progress and logs.

3. **Retrieve the ISO:**
   Upon successful completion, the generated ISO file will be available in the Jenkins workspace.
