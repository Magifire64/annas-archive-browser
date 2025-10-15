# Security Considerations

Anna's [local] Archive is designed for **local, single-user deployment**. The following security considerations should be understood before deployment.

## Default Security Posture

### ✅ Secure by Default for Local Use

- All services run in an isolated Docker network
- Only web UI (port 8000) and torrent client UI (port 8080) are exposed
- No user authentication required (intended for single-user, local access)
- All data stays on your local machine

### ⚠️ Not Secure for Public Access

This application is **NOT designed** for:
- Public internet exposure
- Multi-user environments without authentication
- Production environments accessible beyond localhost

## Security Features

### Network Isolation

All backend services (MariaDB, Elasticsearch) communicate over an internal Docker network and are not directly accessible from outside Docker.

### Database Access

- MariaDB is exposed on port 3306 for debugging purposes
- Default credentials are `annas:annas_archive`
- **Important**: These are development credentials and should be changed if exposing beyond localhost

### Archive Extraction

- File extraction uses safe byte-range reading
- No arbitrary code execution
- Files are served directly without decompression of entire archives

### Input Validation

- File paths are sanitized to prevent directory traversal
- SQL queries use parameterized statements to prevent SQL injection
- Search queries are escaped before database operations

## Security Recommendations

### For Local Use (Default)

1. **Keep it local**: Only access via localhost or localtest.me
2. **Update regularly**: Pull latest changes and rebuild containers
3. **Monitor disk space**: Prevent denial of service through disk exhaustion
4. **Firewall**: Ensure your firewall blocks external access to ports 8000, 8080, 3306, 9200

### If Exposing Beyond Localhost (NOT RECOMMENDED)

If you must expose this application beyond localhost:

1. **Change all default passwords**
   - Edit `docker-compose.yml` to change database passwords
   - Change qBittorrent password immediately after first login

2. **Add authentication**
   - Implement user authentication in the web app
   - Use a reverse proxy (nginx/traefik) with authentication

3. **Use HTTPS**
   - Configure SSL/TLS certificates
   - Use a reverse proxy to handle HTTPS

4. **Restrict database access**
   - Remove the ports section from MariaDB and Elasticsearch in `docker-compose.yml`
   - Only expose services that need external access

5. **Use environment variables**
   - Store credentials in `.env` file (not tracked in git)
   - Never commit credentials to version control

6. **Enable security features**
   - Enable Elasticsearch security (xpack.security.enabled=true)
   - Configure MariaDB with stronger authentication

7. **Regular updates**
   - Keep Docker images updated
   - Monitor security advisories for dependencies

8. **Rate limiting**
   - Implement rate limiting on API endpoints
   - Use fail2ban or similar tools

9. **Logging and monitoring**
   - Enable and monitor access logs
   - Set up alerts for suspicious activity

## Vulnerability Reporting

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email the maintainers privately (see GitHub profile)
3. Provide detailed information about the vulnerability
4. Allow time for a fix before public disclosure

## Known Limitations

### Authentication
- **Status**: Not implemented
- **Impact**: Anyone with access to the web interface has full control
- **Mitigation**: Only use on trusted local networks

### Password Storage
- **Status**: Default credentials in docker-compose.yml
- **Impact**: Credentials visible in configuration files
- **Mitigation**: Change defaults, use .env files

### API Security
- **Status**: No rate limiting or API keys
- **Impact**: Potential for abuse if exposed publicly
- **Mitigation**: Do not expose to public internet

### File Upload
- **Status**: No file upload capability (intentional)
- **Impact**: N/A - files only come from trusted torrents
- **Mitigation**: N/A

## Security Checklist

Before deploying, verify:

- [ ] Application is only accessible from localhost or trusted network
- [ ] Firewall rules are in place
- [ ] Default passwords have been changed (if exposing beyond localhost)
- [ ] Docker daemon is up to date
- [ ] You understand this is not production-ready for public access

## Best Practices

### Docker Security

1. **Keep Docker updated**: `docker version` should show recent version
2. **Scan images**: Use `docker scan` to check for vulnerabilities
3. **Minimize exposed ports**: Only expose what's necessary
4. **Use specific image tags**: Avoid `latest` in production

### Application Security

1. **Regular updates**: `git pull && docker compose up -d --build`
2. **Backup data**: Regular backups of volumes
3. **Monitor logs**: `docker compose logs -f` to watch for issues
4. **Limit disk space**: Set quotas to prevent exhaustion

### Network Security

1. **Local access only**: Bind to 127.0.0.1 if possible
2. **Use VPN**: If accessing remotely, use VPN instead of exposing ports
3. **Firewall rules**: Block external access to all ports except those intentionally exposed

## Disclaimer

This software is provided "as is" without warranty of any kind. Users are responsible for their own security posture when deploying this application. The maintainers are not responsible for any security incidents resulting from improper deployment or configuration.

## Resources

- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/latest/security/)
