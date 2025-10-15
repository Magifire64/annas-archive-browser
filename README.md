# Anna's [local] Archive

A local version of Anna's Archive that allows you to browse and access torrents directly from your own machine.

## Quick Start (One-liner)

Prerequisites: Docker and Docker Compose installed on your system.

```bash
git clone https://github.com/Magifire64/annas-archive-browser.git && cd annas-archive-browser && docker-compose up -d
```

Then navigate to http://localtest.me:8000 in your browser.

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

### Can't access the web interface

Ensure localtest.me resolves to 127.0.0.1. You can also use http://localhost:8000 directly.

### qBittorrent default password

If you need to change the default qBittorrent credentials:
1. Access http://localtest.me:8080
2. Login with admin/adminadmin
3. Go to Tools > Options > Web UI to change the password
