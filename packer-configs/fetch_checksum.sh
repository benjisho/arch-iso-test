#!/bin/bash

# Download the latest checksums
curl -o /tmp/sha256sums.txt https://mirror.rackspace.com/archlinux/iso/latest/sha256sums.txt

# Extract the checksum for the ISO
CHECKSUM=$(grep "archlinux-x86_64.iso" /tmp/sha256sums.txt | awk '{ print $1 }')

# Save the checksum to a temporary file
echo "$CHECKSUM" > /tmp/iso_checksum.txt
