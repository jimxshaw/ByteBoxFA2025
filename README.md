# ByteBox Self-Storage Management System

This project is a rental management system built with:
- **Python** (Flask) for the backend.
- **Jinja2** for the frontend templating.
- **PostgreSQL** for the database.
- **Docker + Docker Compose** for environment portability and ease of use.

---

## Requirements

Before starting, ensure that **Docker Desktop** is installed and running on your machine.

### Install Docker Desktop

Choose your operating system:

- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- [Docker Desktop for Linux](https://docs.docker.com/desktop/install/linux-install/)

Or install Docker Engine via command line (for more advanced Linux setups):

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install docker.io docker-compose

# Fedora / RHEL
sudo dnf install docker docker-compose

# Arch Linux
sudo pacman -S docker docker-compose
```

## Setup Instructions (assuming Docker Desktop is running)

1. Allow execution of the initializer script

  Give the initialize.sh script execution permission:
  
  ```bash
  chmod +x initialize.sh
  ```

2. Run the initialization script

  ```bash
  ./initialize.sh
  ```

  Or if you're on Windows and using PowerShell or the Command Prompt use

  ```sh
  bash ./initialize.sh
  ```

  This script will:

    - Tear down, build and run the necessary Docker containers.
    - Set up the database.
    - Launch the application on *http://localhost:5000*.
    - Log into the database and allow you to run SQL queries and other commands.
