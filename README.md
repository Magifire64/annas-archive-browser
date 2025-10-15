# Anna's [local] Archive

```
 ╔═══════════════════════════════════════════════════╗
 ║   Anna's [local] Archive                          ║
 ║   Browse your local torrents collection           ║
 ╚═══════════════════════════════════════════════════╝
```

A local version of Anna's Archive that allows you to browse and access torrents directly from your own machine.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)](https://www.docker.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**New to this project?** Check out the [Quick Start Guide](QUICKSTART.md) for a 5-minute setup!

## Quick Start (One-liner)

Prerequisites: Docker and Docker Compose installed on your system.

### Linux / macOS
```bash
git clone https://github.com/Magifire64/annas-archive-browser.git && cd annas-archive-browser && ./start.sh
```

### Windows
```cmd
git clone https://github.com/Magifire64/annas-archive-browser.git && cd annas-archive-browser && start.bat
```

Alternatively, for all platforms:
```bash
git clone https://github.com/Magifire64/annas-archive-browser.git && cd annas-archive-browser && docker compose up -d
```

Then navigate to http://localtest.me:8000 or http://localhost:8000 in your browser.

## Installation

### Prerequisites

1. **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
   - Windows: [Download Docker Desktop](https://docs.docker.com/desktop/windows/install/)
   - Mac: [Download Docker Desktop](https://docs.docker.com/desktop/mac/install/)
   - Linux: [Install Docker Engine](https://docs.docker.com/engine/install/)

2. **Docker Compose** (usually included with Docker Desktop)
   - Verify: `docker compose version` or `docker-compose version`

3. **Git** (for cloning the repository)
   - [Download Git](https://git-scm.com/downloads)

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Magifire64/annas-archive-browser.git
   cd annas-archive-browser
   ```

2. **Start the services**
   
   Using the quick start script (recommended):
   ```bash
   # Linux/Mac
   ./start.sh
   
   # Windows
   start.bat
   ```
   
   Or manually with Docker Compose:
   ```bash
   docker compose up -d --build
   ```

3. **Wait for services to initialize** (30-60 seconds)

4. **Access the web interface**
   - Open your browser to http://localhost:8000
   - Or use http://localtest.me:8000

5. **Verify installation** (Linux/Mac only)
   ```bash
   ./test.sh
   ```

## What's Included

- **Web Interface**: Browse and search your local archive at http://localtest.me:8000
- **Torrent Downloader**: qBittorrent with web UI at http://localtest.me:8080
- **Database Services**: MariaDB and Elasticsearch for metadata storage
- **File Indexing**: Automatic and manual indexing of local files
- **Archive Extraction**: Direct file access from within archives using byte offsets

## Features

### Metadata Management
- One-click download of the latest aa_derived_mirror_metadata
- One-click loading of metadata into databases

### Torrent Management
- View list of all available torrents from Anna's Archive
- Easy selection and download of entire ranges
- Generate torrent lists based on available disk space

### File Access
- Search filter for "local files" to see only files you have
- Download button for locally available files
- Direct extraction from archives without full extraction

### Branding
- Consistent "Anna's [local] Archive" branding throughout
- Local-optimized interface with non-functional remote features disabled

## Configuration

### Using Your Own Torrent Directory

If you already have torrents downloaded, you can point the installation to your existing directory:

1. Edit `docker-compose.yml`
2. Change the `torrents_data` volume mapping for the `webapp` service:
   ```yaml
   volumes:
     - /path/to/your/torrents:/data/torrents
   ```

### Accessing Services

- **Web Interface**: http://localtest.me:8000
- **qBittorrent Web UI**: http://localtest.me:8080 (default credentials: admin/adminadmin)
- **Elasticsearch**: http://localhost:9200
- **MariaDB**: localhost:3306

## Manual Operations

### Indexing Files

Files are automatically indexed when torrents complete. To manually index:

1. Go to http://localtest.me:8000/admin
2. Click "Index Local Files"

### Downloading Metadata

1. Go to http://localtest.me:8000/admin
2. Click "Download aa_derived_mirror_metadata"
3. Click "Load Metadata into Databases"

## Stopping the Service

```bash
docker-compose down
```

To remove all data:

```bash
docker-compose down -v
```

## Requirements

- Docker 20.10 or newer
- Docker Compose 2.0 or newer
- At least 4GB RAM
- Sufficient disk space for torrents and metadata

## Troubleshooting

### Services won't start

Check service health:
```bash
docker-compose ps
```

View logs:
```bash
docker-compose logs webapp
docker-compose logs mariadb
docker-compose logs elasticsearch
```

Run the test script:
```bash
./test.sh
```

### Can't access the web interface

Ensure localtest.me resolves to 127.0.0.1. You can also use http://localhost:8000 directly.

### qBittorrent default password

If you need to change the default qBittorrent credentials:
1. Access http://localtest.me:8080
2. Login with admin/adminadmin
3. Go to Tools > Options > Web UI to change the password

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute getting started guide (start here!)
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture and design
- [SECURITY.md](SECURITY.md) - Security considerations and best practices
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute to the project
- [agentinstructions.txt](agentinstructions.txt) - Original requirements

## Frequently Asked Questions (FAQ)

### How much disk space do I need?

It depends on how many torrents you want to download. Start with at least 100GB free space. The metadata itself is relatively small (a few GB), but the actual torrents can be very large.

### Can I use this without downloading any torrents?

Yes! You can browse the metadata and search functionality without downloading torrents. However, you won't be able to download actual files until you've downloaded and indexed torrents.

### How do I add more torrents?

1. Go to the Admin panel at http://localhost:8000/admin
2. Click "Load Available Torrents" to see all available torrents
3. Copy the torrent URLs
4. Add them to qBittorrent at http://localhost:8080
5. Once downloaded, files are automatically indexed

### Where are my downloaded files stored?

By default, files are stored in a Docker volume. To access them directly or use your existing torrents:

1. Edit `docker-compose.yml`
2. Change the `torrents_data` volume mapping under the `webapp` service
3. Replace with: `/path/to/your/torrents:/data/torrents`

### How do I update the metadata?

1. Go to http://localhost:8000/admin
2. Click "Download aa_derived_mirror_metadata"
3. Wait for the download to complete
4. Click "Load Metadata into Databases"

### Why "Anna's [local] Archive"?

The [local] designation distinguishes this self-hosted instance from the main Anna's Archive website. It emphasizes that you're browsing your own local collection.

### Can multiple people use this?

The system is designed for single-user use. For multi-user scenarios, you'd need to add authentication and user management (not currently implemented).

### How do I backup my installation?

```bash
# Stop the services
docker compose down

# Backup the volumes
docker run --rm -v annas-archive-browser_mariadb_data:/data -v $(pwd):/backup ubuntu tar czf /backup/mariadb-backup.tar.gz /data
docker run --rm -v annas-archive-browser_es_data:/data -v $(pwd):/backup ubuntu tar czf /backup/es-backup.tar.gz /data
docker run --rm -v annas-archive-browser_torrents_data:/data -v $(pwd):/backup ubuntu tar czf /backup/torrents-backup.tar.gz /data

# Restart services
docker compose up -d
```

### How do I uninstall?

```bash
# Stop and remove all containers, networks, and volumes
docker compose down -v

# Remove cloned repository
cd ..
rm -rf annas-archive-browser
```

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
