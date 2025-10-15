import os
import json
import hashlib
import requests
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, Response
from flask_cors import CORS
from elasticsearch import Elasticsearch
import MySQLdb
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
MARIADB_HOST = os.getenv('MARIADB_HOST', 'localhost')
MARIADB_PORT = int(os.getenv('MARIADB_PORT', 3306))
MARIADB_USER = os.getenv('MARIADB_USER', 'annas')
MARIADB_PASSWORD = os.getenv('MARIADB_PASSWORD', 'annas_archive')
MARIADB_DATABASE = os.getenv('MARIADB_DATABASE', 'annas_archive')
ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST', 'localhost')
ELASTICSEARCH_PORT = int(os.getenv('ELASTICSEARCH_PORT', 9200))
TORRENTS_PATH = os.getenv('TORRENTS_PATH', '/data/torrents')
METADATA_PATH = '/data/metadata'

# Initialize connections
es = None
db_conn = None

def get_es():
    global es
    if es is None:
        es = Elasticsearch([f'http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'])
    return es

def get_db():
    global db_conn
    if db_conn is None or not db_conn.open:
        db_conn = MySQLdb.connect(
            host=MARIADB_HOST,
            port=MARIADB_PORT,
            user=MARIADB_USER,
            passwd=MARIADB_PASSWORD,
            db=MARIADB_DATABASE
        )
    return db_conn

def init_database():
    """Initialize database tables"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Create files index table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS local_files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_path VARCHAR(1024) NOT NULL,
                filename VARCHAR(512) NOT NULL,
                file_size BIGINT,
                torrent_name VARCHAR(512),
                indexed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_path (file_path(768)),
                INDEX idx_filename (filename(255)),
                INDEX idx_torrent (torrent_name(255))
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create archive byte offsets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS archive_offsets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                archive_path VARCHAR(1024) NOT NULL,
                file_name VARCHAR(512) NOT NULL,
                byte_offset BIGINT NOT NULL,
                byte_length BIGINT NOT NULL,
                INDEX idx_archive (archive_path(255)),
                INDEX idx_file (file_name(255))
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Database initialization error: {e}")

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/search')
def search():
    """Search page with local files filter"""
    query = request.args.get('q', '')
    local_only = request.args.get('local', 'false') == 'true'
    page = int(request.args.get('page', 1))
    per_page = 25
    
    results = []
    total = 0
    
    if query:
        if local_only:
            # Search only local files
            results, total = search_local_files(query, page, per_page)
        else:
            # Search all (would normally query Elasticsearch with all data)
            results, total = search_all_files(query, page, per_page)
    
    return render_template('search.html', 
                         query=query, 
                         results=results, 
                         total=total,
                         page=page,
                         per_page=per_page,
                         local_only=local_only)

def search_local_files(query, page, per_page):
    """Search in local files database"""
    try:
        conn = get_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        offset = (page - 1) * per_page
        search_pattern = f"%{query}%"
        
        # Get total count
        cursor.execute("""
            SELECT COUNT(*) as total FROM local_files 
            WHERE filename LIKE %s
        """, (search_pattern,))
        total = cursor.fetchone()['total']
        
        # Get results
        cursor.execute("""
            SELECT * FROM local_files 
            WHERE filename LIKE %s
            ORDER BY filename
            LIMIT %s OFFSET %s
        """, (search_pattern, per_page, offset))
        
        results = cursor.fetchall()
        cursor.close()
        
        return results, total
    except Exception as e:
        print(f"Search error: {e}")
        return [], 0

def search_all_files(query, page, per_page):
    """Search all files (placeholder - would use Elasticsearch)"""
    # For now, just return local files
    return search_local_files(query, page, per_page)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    """Download a local file"""
    try:
        conn = get_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM local_files WHERE id = %s", (file_id,))
        file_info = cursor.fetchone()
        cursor.close()
        
        if file_info and os.path.exists(file_info['file_path']):
            return send_file(file_info['file_path'], 
                           as_attachment=True,
                           download_name=file_info['filename'])
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-from-archive')
def download_from_archive():
    """Extract and download a file from an archive using byte offsets"""
    archive_path = request.args.get('archive')
    file_name = request.args.get('file')
    
    try:
        conn = get_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT * FROM archive_offsets 
            WHERE archive_path = %s AND file_name = %s
        """, (archive_path, file_name))
        offset_info = cursor.fetchone()
        cursor.close()
        
        if not offset_info or not os.path.exists(archive_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Read the specific bytes from the archive
        with open(archive_path, 'rb') as f:
            f.seek(offset_info['byte_offset'])
            data = f.read(offset_info['byte_length'])
        
        return Response(data, 
                       mimetype='application/octet-stream',
                       headers={'Content-Disposition': f'attachment; filename={file_name}'})
    except Exception as e:
        print(f"Archive extraction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin')
def admin():
    """Admin page for metadata and indexing operations"""
    return render_template('admin.html')

@app.route('/api/torrents')
def api_torrents():
    """Get list of available torrents from Anna's Archive"""
    try:
        response = requests.get('https://annas-archive.org/dyn/torrents.json', timeout=10)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-metadata', methods=['POST'])
def api_download_metadata():
    """Download aa_derived_mirror_metadata"""
    try:
        # This is a placeholder - actual URL would need to be determined
        # from the torrents.json or another source
        metadata_url = "https://annas-archive.org/dyn/small_file/torrents/managed_by_aa/annas_archive_data__aacid/annas_archive_data__aacid__ia2_acsmpdf_files__20231102T181139Z--20231102T185436Z.jsonl.zst.torrent"
        
        # In practice, this would download the actual metadata file
        # For now, just acknowledge the request
        return jsonify({'status': 'started', 'message': 'Metadata download initiated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load-metadata', methods=['POST'])
def api_load_metadata():
    """Load metadata into databases"""
    try:
        # This would load the downloaded metadata into ES and MariaDB
        # Placeholder for actual implementation
        return jsonify({'status': 'started', 'message': 'Metadata loading initiated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/index-files', methods=['POST'])
def api_index_files():
    """Manually trigger file indexing"""
    try:
        indexed_count = index_local_files()
        return jsonify({'status': 'completed', 'files_indexed': indexed_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def index_local_files():
    """Index all files in the torrents directory"""
    conn = get_db()
    cursor = conn.cursor()
    indexed_count = 0
    
    try:
        torrents_path = Path(TORRENTS_PATH)
        if not torrents_path.exists():
            return 0
        
        for file_path in torrents_path.rglob('*'):
            if file_path.is_file():
                try:
                    # Get relative path and torrent name
                    rel_path = file_path.relative_to(torrents_path)
                    torrent_name = rel_path.parts[0] if len(rel_path.parts) > 1 else None
                    
                    # Insert or update in database
                    cursor.execute("""
                        INSERT INTO local_files (file_path, filename, file_size, torrent_name)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE 
                            file_size = VALUES(file_size),
                            indexed_at = CURRENT_TIMESTAMP
                    """, (str(file_path), file_path.name, file_path.stat().st_size, torrent_name))
                    
                    indexed_count += 1
                except Exception as e:
                    print(f"Error indexing {file_path}: {e}")
                    continue
        
        conn.commit()
    finally:
        cursor.close()
    
    return indexed_count

@app.route('/api/stats')
def api_stats():
    """Get statistics about the local archive"""
    try:
        conn = get_db()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("SELECT COUNT(*) as total, SUM(file_size) as total_size FROM local_files")
        stats = cursor.fetchone()
        cursor.close()
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Wait for services to be ready
    import time
    max_retries = 30
    for i in range(max_retries):
        try:
            get_db()
            init_database()
            print("Database initialized successfully")
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Waiting for database... ({i+1}/{max_retries})")
                time.sleep(2)
            else:
                print(f"Failed to connect to database: {e}")
                raise
    
    # Run the application
    app.run(host='0.0.0.0', port=8000, debug=False)
