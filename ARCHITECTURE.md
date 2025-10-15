# Anna's [local] Archive - Architecture

## Overview

Anna's [local] Archive is a Docker-based solution for running a local instance of Anna's Archive. It allows users to browse, search, and download files from their own torrents collection.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     User Browser                         │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ├─────────> http://localhost:8000 (Web UI)
                   └─────────> http://localhost:8080 (qBittorrent UI)
                   
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │              Web Application (Flask)            │    │
│  │  - Search & Browse                              │    │
│  │  - File Indexing                                │    │
│  │  - Metadata Management                          │    │
│  │  - Archive Extraction Proxy                     │    │
│  └──────┬─────────────┬────────────┬────────────┬──┘    │
│         │             │            │            │       │
│    ┌────▼────┐   ┌────▼────┐  ┌───▼────┐  ┌────▼────┐ │
│    │ MariaDB │   │   ES    │  │ qBit   │  │ Volumes │ │
│    │         │   │         │  │ torrent│  │         │ │
│    └─────────┘   └─────────┘  └────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. Web Application (Flask)

**Purpose**: Main user interface and API server

**Responsibilities**:
- Serve web pages with "Anna's [local] Archive" branding
- Handle search queries (local and global)
- Index files from the torrents directory
- Serve files to users
- Extract files from archives using byte offsets
- Manage metadata downloads and loading

**Technology**: Python 3.11, Flask, Gunicorn

**Endpoints**:
- `/` - Home page
- `/search` - Search interface
- `/admin` - Admin panel
- `/download/<id>` - Download local files
- `/download-from-archive` - Extract from archives
- `/api/torrents` - List available torrents
- `/api/download-metadata` - Download metadata
- `/api/load-metadata` - Load metadata into databases
- `/api/index-files` - Trigger file indexing
- `/api/stats` - Get statistics
- `/health` - Health check

### 2. MariaDB

**Purpose**: Relational database for structured data

**Responsibilities**:
- Store file index (paths, names, sizes)
- Store archive byte offset mappings
- Store metadata records

**Tables**:
- `local_files`: Index of all local files
  - `id`, `file_path`, `filename`, `file_size`, `torrent_name`, `indexed_at`
- `archive_offsets`: Byte offset mappings for archive extraction
  - `id`, `archive_path`, `file_name`, `byte_offset`, `byte_length`

### 3. Elasticsearch

**Purpose**: Full-text search and indexing

**Responsibilities**:
- Index metadata for fast searching
- Provide search capabilities across all metadata fields
- Support advanced filtering and aggregations

**Indices** (planned):
- `files`: File metadata
- `torrents`: Torrent metadata

### 4. qBittorrent

**Purpose**: Torrent client with web UI

**Responsibilities**:
- Download torrents
- Seed downloaded content
- Provide web interface for torrent management
- Trigger indexing on completion (planned)

**Configuration**:
- Web UI port: 8080
- Default credentials: admin/adminadmin
- Download directory: `/data/torrents` (shared volume)

## Data Flow

### File Indexing Flow

```
1. Torrent completes download
   ↓
2. Files saved to /data/torrents
   ↓
3. User triggers indexing (manual or automatic)
   ↓
4. Web app scans /data/torrents recursively
   ↓
5. File metadata inserted into MariaDB
   ↓
6. Files now searchable via local filter
```

### Search Flow

```
1. User enters search query
   ↓
2. Web app queries MariaDB (if local_only=true)
   OR
   Web app queries Elasticsearch (if local_only=false)
   ↓
3. Results returned with local availability indicator
   ↓
4. User can download local files directly
```

### Archive Extraction Flow

```
1. User requests file from archive
   ↓
2. Web app queries archive_offsets table
   ↓
3. Opens archive file and seeks to byte_offset
   ↓
4. Reads byte_length bytes
   ↓
5. Streams file to user
```

## Storage Volumes

- `mariadb_data`: MariaDB database files (persistent)
- `es_data`: Elasticsearch indices (persistent)
- `qbittorrent_config`: qBittorrent configuration (persistent)
- `torrents_data`: Downloaded torrent files (persistent, can be mapped to existing directory)

## Security Considerations

- All services run in isolated Docker network
- Only web UI (8000) and torrent client UI (8080) are exposed
- Database credentials are set via environment variables
- No external network access required for core functionality
- Archive extraction uses safe byte-range reading (no arbitrary code execution)

## Performance Considerations

### Indexing
- File indexing does NOT compute MD5 hashes (too slow)
- Only indexes filenames, paths, and sizes
- Uses database transactions for bulk inserts
- Can handle millions of files

### Search
- MariaDB for simple filename searches (fast)
- Elasticsearch for complex metadata searches (when implemented)
- Pagination to handle large result sets

### File Serving
- Direct file serving for standalone files
- Byte-range seeking for archive extraction
- No full archive extraction needed

## Scalability

The system is designed for single-user, single-machine deployment:

- **Storage**: Limited by available disk space
- **Memory**: Minimum 4GB RAM recommended
- **CPU**: Indexing is CPU-light, scales with file count
- **Network**: All communication is local (except torrent downloads)

## Future Enhancements

1. **Automatic Indexing**: Watch directory for new files
2. **Metadata Integration**: Full integration with aa_derived_mirror_metadata
3. **Advanced Search**: Utilize Elasticsearch for rich queries
4. **Multi-user Support**: Authentication and user profiles
5. **API**: RESTful API for programmatic access
6. **Mobile App**: Companion mobile application
7. **Backup/Restore**: Easy backup and restore of indices
8. **Statistics Dashboard**: Detailed usage and storage statistics

## Development

### Running Locally

```bash
docker compose up --build
```

### Viewing Logs

```bash
docker compose logs -f webapp
```

### Database Access

```bash
docker compose exec mariadb mysql -uannas -pannas_archive annas_archive
```

### Elasticsearch Access

```bash
curl http://localhost:9200/_cat/indices?v
```

## Troubleshooting

### Services won't start
- Check Docker daemon is running
- Check port availability (8000, 8080, 3306, 9200)
- Review logs: `docker compose logs`

### Database connection errors
- Wait 30-60 seconds for MariaDB to fully initialize
- Check healthcheck: `docker compose ps`

### Files not appearing in search
- Ensure files are in `/data/torrents`
- Trigger manual indexing from Admin panel
- Check logs for indexing errors
