# Changelog

All notable changes to Anna's [local] Archive will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-15

### Added
- Initial release of Anna's [local] Archive
- Docker Compose setup with MariaDB, Elasticsearch, qBittorrent, and Flask web app
- Web interface with "Anna's [local] Archive" branding
- Home page with statistics and quick links
- Search functionality with local files filter
- Admin panel for metadata and file management
- File indexing system for local torrents
- Direct file download from local storage
- Archive extraction proxy using byte offsets (framework)
- Health check endpoints for monitoring
- One-liner installation scripts for Linux/Mac and Windows
- Comprehensive documentation (README, QUICKSTART, ARCHITECTURE, SECURITY, CONTRIBUTING)
- Test script for validating installation
- Configuration examples (.env.example, docker-compose.override.example.yml)
- FAQ section in README
- MIT License

### Features
- **One-liner Setup**: Install and run with a single command on Windows, Mac, or Linux
- **Torrent Integration**: Built-in qBittorrent with web UI for downloading torrents
- **Local Files Filter**: Search specifically for files you have locally
- **Metadata Management**: Download and load Anna's Archive metadata
- **File Serving**: Direct download of local files with proper branding
- **Archive Extraction**: Extract files from archives without full decompression (framework)
- **Statistics Dashboard**: View file counts and storage usage
- **Health Monitoring**: Check status of all services

### Documentation
- README.md with installation instructions and FAQ
- QUICKSTART.md for 5-minute setup guide
- ARCHITECTURE.md explaining system design
- SECURITY.md with security best practices
- CONTRIBUTING.md for contributors
- LICENSE (MIT)

### Technical Details
- Python 3.11 with Flask web framework
- MariaDB 11 for structured data storage
- Elasticsearch 8.11 for full-text search
- qBittorrent for torrent management
- Docker Compose for orchestration
- Health checks on all services
- Automatic database initialization

### Known Limitations
- Metadata download is placeholder (URL needs configuration)
- Metadata loading is placeholder (needs implementation)
- Archive byte offset extraction is framework only
- No authentication system (designed for single-user local use)
- No automatic indexing on torrent completion (manual only)
- Elasticsearch not fully integrated for search

## [Unreleased]

### Planned Features
- Automatic file indexing on torrent completion
- Full integration with aa_derived_mirror_metadata
- Complete archive extraction using byte offsets
- Advanced Elasticsearch queries
- Improved metadata management
- Better error handling and user feedback
- Progress indicators for long-running operations
- API documentation

### Future Enhancements
- Multi-user support with authentication
- Mobile-responsive design improvements
- REST API for programmatic access
- Backup and restore functionality
- Advanced search filters
- File preview capabilities
- Torrent selection based on disk space
- Integration with external torrent clients
