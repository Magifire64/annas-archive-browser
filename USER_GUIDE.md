# User Guide - Anna's [local] Archive

## Interface Overview

### Main Navigation

Every page includes a header with:
- **Anna's [local] Archive** - Main branding
- **Home** - Return to home page
- **Search** - Search your collection
- **Admin** - Administrative functions
- **Torrent Client** - Opens qBittorrent UI in new tab

## Page Descriptions

### Home Page (/)

The landing page shows:

1. **Welcome Section**
   - Introduction to Anna's [local] Archive
   - Search box for quick searches
   - "Show only local files" checkbox (checked by default)

2. **Quick Stats**
   - Number of local files indexed
   - Total storage size in GB
   - Updates automatically

3. **Getting Started Guide**
   - Step-by-step instructions for new users
   - Links to Admin panel and Torrent Client

### Search Page (/search)

Search your local collection:

1. **Search Box**
   - Text input for search queries
   - "Show only local files" filter checkbox
   - Search button

2. **Results Display**
   For each result:
   - Filename (prominent)
   - "Local" badge in green
   - File size in MB
   - Torrent name (if part of a torrent)
   - Indexed timestamp
   - Download button: "Download from Anna's [local] Archive"

3. **Pagination**
   - 25 results per page
   - Previous/Next navigation
   - Page numbers

### Admin Panel (/admin)

Manage your archive:

1. **Metadata Management**
   - "Download aa_derived_mirror_metadata" button
   - "Load Metadata into Databases" button
   - Status messages after actions

2. **File Indexing**
   - "Index Local Files" button
   - Shows number of files indexed
   - Status updates

3. **Available Torrents**
   - "Load Available Torrents" button
   - Table showing:
     - Torrent name
     - Size
     - Download URL
   - Instructions to add to qBittorrent

4. **Archive Statistics**
   - Total local files
   - Total storage size
   - Updates after indexing

### qBittorrent UI (/torrent-client or :8080)

External torrent management interface:

1. **Login**
   - Username: admin
   - Password: adminadmin (change immediately!)

2. **Add Torrents**
   - Click "+" button
   - Paste torrent URL or upload .torrent file
   - Select download location

3. **Manage Downloads**
   - View active/completed torrents
   - Control seeding
   - Delete torrents

## User Flows

### First-Time Setup

```
1. Install and start → Home page
2. Go to Admin panel
3. (Optional) Download and load metadata
4. Open Torrent Client
5. Add torrents to download
6. Wait for downloads
7. Index files from Admin panel
8. Search for files
```

### Daily Use

```
1. Open Home page
2. Use search box
3. Enable "Show only local files"
4. Click search
5. Browse results
6. Download files with one click
```

### Adding New Content

```
1. Go to Admin panel
2. Load Available Torrents
3. Copy torrent URLs
4. Open Torrent Client
5. Add torrents
6. Wait for downloads
7. Index new files
8. Search and use
```

## Tips

### Searching Effectively
- Use specific terms for better results
- Keep "local files" filter on for instant results
- Check spelling if no results

### Managing Storage
- Monitor total size on Home page
- Remove unwanted torrents from qBittorrent
- Keep files you want to seed

### Indexing
- Index after downloading new torrents
- Re-index if files seem missing
- Indexing is fast (no MD5 computation)

### Troubleshooting
- Check Admin panel statistics if files missing
- Re-index if search seems incomplete
- View logs with: `docker compose logs -f webapp`

## Keyboard Shortcuts

Currently, standard browser shortcuts apply:
- `Ctrl/Cmd + F` - Find in page
- `Ctrl/Cmd + L` - Focus address bar
- `Alt + Left` - Browser back

## Customization

### Changing Ports

Edit `docker-compose.yml` or create `docker-compose.override.yml`:

```yaml
services:
  webapp:
    ports:
      - "9000:8000"  # Change 9000 to your preferred port
```

### Using Existing Torrents

Edit the webapp volumes in `docker-compose.yml`:

```yaml
services:
  webapp:
    volumes:
      - /your/torrents/path:/data/torrents
```

### Environment Variables

Copy `.env.example` to `.env` and customize:
- Database credentials
- Service hostnames
- Paths

## Advanced Features

### Health Monitoring

Check system health at `/health`:
- Returns JSON with service status
- "healthy" = all services working
- "degraded" = some services have issues

### API Endpoints

Available for programmatic access:
- `/api/stats` - Get statistics
- `/api/torrents` - List available torrents
- `/api/index-files` - Trigger indexing
- `/api/download-metadata` - Download metadata
- `/api/load-metadata` - Load metadata

### Direct File Access

Files can be downloaded by ID:
- `/download/<file_id>` - Download by database ID

Archive extraction (when implemented):
- `/download-from-archive?archive=<path>&file=<name>`

## Getting Help

- Check [QUICKSTART.md](QUICKSTART.md) for setup issues
- Review [FAQ in README.md](README.md#frequently-asked-questions-faq)
- See [TROUBLESHOOTING in README.md](README.md#troubleshooting)
- Open an issue on GitHub for bugs or questions

## Updates and Maintenance

### Updating Anna's [local] Archive

```bash
# Stop services
docker compose down

# Pull latest changes
git pull

# Rebuild and restart
docker compose up -d --build
```

### Backup Your Data

```bash
# Export database
docker compose exec mariadb mysqldump -uannas -pannas_archive annas_archive > backup.sql

# Copy torrents (if using volume)
docker run --rm -v annas-archive-browser_torrents_data:/data -v $(pwd):/backup ubuntu tar czf /backup/torrents.tar.gz /data
```

### Restore from Backup

```bash
# Import database
docker compose exec -T mariadb mysql -uannas -pannas_archive annas_archive < backup.sql

# Restore torrents
docker run --rm -v annas-archive-browser_torrents_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/torrents.tar.gz -C /
```
