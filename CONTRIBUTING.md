# Contributing to Anna's [local] Archive

Thank you for your interest in contributing to Anna's [local] Archive!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Magifire64/annas-archive-browser.git
   cd annas-archive-browser
   ```

2. Start the development environment:
   ```bash
   docker-compose up --build
   ```

3. The web application will be available at http://localhost:8000

## Project Structure

```
annas-archive-browser/
├── docker-compose.yml          # Docker Compose configuration
├── webapp/                     # Main web application
│   ├── Dockerfile             # Application container definition
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── templates/             # HTML templates
│       ├── base.html          # Base template
│       ├── index.html         # Home page
│       ├── search.html        # Search results
│       └── admin.html         # Admin panel
├── README.md                  # Main documentation
├── start.sh                   # Quick start script (Linux/Mac)
└── start.bat                  # Quick start script (Windows)
```

## Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes in the appropriate files

3. Test your changes locally:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. Push to your fork and create a pull request

## Coding Standards

- Use 4 spaces for indentation in Python files
- Follow PEP 8 style guide for Python code
- Keep functions focused and single-purpose
- Add comments for complex logic
- Update documentation when adding new features

## Areas for Contribution

- **Metadata Management**: Improve downloading and loading of metadata
- **File Indexing**: Enhance the file indexing system
- **Archive Extraction**: Implement byte-offset based extraction
- **Search**: Improve search functionality and filters
- **UI/UX**: Enhance the user interface
- **Documentation**: Improve setup and usage documentation
- **Testing**: Add unit and integration tests

## Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the issue tracker
2. If not, create a new issue with:
   - Clear description of the problem or feature
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - System information (OS, Docker version, etc.)

## Questions?

Feel free to open an issue for questions or discussions about the project.
