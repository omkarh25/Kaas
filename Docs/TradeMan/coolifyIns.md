The provided URL contains the installation guide for **Coolify**, a self-hosted platform for managing applications. Here’s a summary of the key points from the documentation:

## Requirements

### Supported Operating Systems
- **Debian-based**: Debian, Ubuntu, etc.
- **Redhat-based**: CentOS, Fedora, Redhat, AlmaLinux, Rocky, etc.
- **SUSE-based**: SLES, SUSE, openSUSE, etc.
- **Arch Linux**
- **Raspberry Pi OS** (Raspbian)

### Supported Architectures
- **AMD64**
- **ARM64**

### Minimum Server Specifications
- **For Coolify**: 
  - 2 CPUs
  - 2 GB RAM
  - 30+ GB storage
- Additional resources may be required based on usage.

## Installation Methods

### Automated Installation
1. Ensure SSH is enabled and accessible.
2. Ensure `curl` is installed on your server.
3. Execute the installation command as the root user.
4. Access Coolify via `http://<ip>:8000`.

### Manual Installation
1. Follow steps similar to the automated method but manually install Docker and set up directories and configuration files.
2. Generate an SSH key for Coolify.
3. Start Coolify and access it through the same URL.

### Docker Desktop (Windows)
1. Install Docker Desktop and create a directory for Coolify data.
2. Copy and rename the necessary configuration files.
3. Create a Docker network for Coolify.
4. Start with `docker compose up` and access via `localhost:8000`.

This guide provides comprehensive steps to set up Coolify on various platforms, ensuring users can efficiently manage their applications in a self-hosted environment.

Citations:
[1] https://coolify.io/docs/installation