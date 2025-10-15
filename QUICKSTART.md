# Anna's [local] Archive - Quick Start Guide

This guide will help you get started with Anna's [local] Archive in 5 minutes.

## Installation (2 minutes)

1. **Install Docker Desktop** if you haven't already
   - [Windows](https://docs.docker.com/desktop/windows/install/)
   - [Mac](https://docs.docker.com/desktop/mac/install/)
   - [Linux](https://docs.docker.com/engine/install/)

2. **Clone and start**
   ```bash
   git clone https://github.com/Magifire64/annas-archive-browser.git
   cd annas-archive-browser
   ./start.sh  # or start.bat on Windows
   ```

3. **Wait for services to start** (30-60 seconds)

## First Use (3 minutes)

### Step 1: Access the Web Interface

Open your browser and go to: http://localhost:8000

You should see the Anna's [local] Archive home page.

### Step 2: Check the Admin Panel

1. Click on **Admin** in the navigation bar
2. You'll see options for:
   - Downloading metadata
   - Loading metadata into databases
   - Indexing local files
   - Viewing available torrents

### Step 3: Download Your First Torrent

1. In the Admin panel, click **"Load Available Torrents"**
2. You'll see a list of available torrents from Anna's Archive
3. Pick a torrent URL and copy it
4. Open qBittorrent at http://localhost:8080
   - Default login: `admin` / `adminadmin`
5. Click the "+" button to add a torrent
6. Paste the URL and click "Download"

### Step 4: Index Your Files

Once a torrent finishes downloading (or if you already have files):

1. Go back to http://localhost:8000/admin
2. Click **"Index Local Files"**
3. Wait for indexing to complete
4. Check the stats on the home page to see your files

### Step 5: Search Your Collection

1. Go to the home page or click **Search**
2. Enter a search term
3. Make sure **"Show only local files"** is checked
4. Click **Search**
5. You'll see results from your local collection
6. Click **"Download from Anna's [local] Archive"** to download files

## Next Steps

### Download Metadata (Optional)

For better search and more information about files:

1. Go to Admin panel
2. Click **"Download aa_derived_mirror_metadata"**
3. Once complete, click **"Load Metadata into Databases"**
4. This will enhance search with full metadata

### Use Your Existing Torrents

If you already have torrents downloaded:

1. Stop the services: `docker compose down`
2. Edit `docker-compose.yml`
3. Under the `webapp` service, find the `volumes` section
4. Change `torrents_data:/data/torrents` to `/your/path:/data/torrents`
5. Start again: `docker compose up -d`
6. Index the files from the Admin panel

### Customize Settings

1. Copy `.env.example` to `.env`
2. Edit `.env` with your preferences
3. Restart: `docker compose down && docker compose up -d`

## Tips and Tricks

### Faster Searches
- Use specific terms rather than generic words
- Filter by local files only for instant results
- Use quotes for exact phrases (when implemented)

### Managing Disk Space
- Monitor your disk space regularly
- Delete completed torrents you don't need in qBittorrent
- Keep seeding torrents you want to share

### Keeping Everything Updated
```bash
# Stop services
docker compose down

# Pull latest changes
git pull

# Rebuild and start
docker compose up -d --build
```

### Viewing Logs
```bash
# All services
docker compose logs -f

# Just the web app
docker compose logs -f webapp

# Just qBittorrent
docker compose logs -f qbittorrent
```

### Checking Service Health
```bash
# See all running services
docker compose ps

# Run test script (Linux/Mac)
./test.sh
```

## Common Issues

### "Connection refused" errors
- Wait 30-60 seconds for services to fully start
- Check logs: `docker compose logs webapp`

### Files not showing in search
- Make sure you've indexed: Admin → Index Local Files
- Check the torrents directory has files
- Verify permissions on the torrents directory

### qBittorrent not accessible
- Make sure port 8080 is not in use
- Check logs: `docker compose logs qbittorrent`
- Try restarting: `docker compose restart qbittorrent`

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
- Open an issue on GitHub for bugs or questions

## Stopping and Cleanup

### Stop services (keeps data)
```bash
docker compose down
```

### Stop and remove all data
```bash
docker compose down -v
```

### Remove everything
```bash
docker compose down -v
cd ..
rm -rf annas-archive-browser
```

---

**Congratulations!** You now have Anna's [local] Archive up and running. Happy browsing! 📚
