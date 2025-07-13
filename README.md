# 📸 Photo Upload Gallery

A beautiful and modern web application for uploading, viewing, and managing photos. Built with Flask and featuring a responsive design with drag-and-drop functionality.

## ✨ Features

- **Drag & Drop Upload**: Simply drag photos onto the upload area or click to browse
- **Multiple File Support**: Upload multiple photos at once
- **Image Gallery**: View all uploaded photos in a beautiful grid layout
- **Photo Management**: View full-size images and delete unwanted photos
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **File Validation**: Supports PNG, JPG, JPEG, GIF, and WebP formats
- **Security**: Secure file handling with unique filename generation
- **Real-time Feedback**: Success/error messages and loading indicators

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd website.py
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5001
   ```

## 📁 Project Structure

```
website.py/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── templates/         # HTML templates
│   └── index.html     # Main page template
└── uploads/           # Uploaded photos (created automatically)
```

## 🎨 How to Use

### Uploading Photos

1. **Drag & Drop**: Simply drag photos from your computer onto the upload area
2. **Click to Browse**: Click the upload area to open a file browser
3. **Select Files**: Choose one or multiple image files
4. **Upload**: Click the "Upload Photo" button

### Managing Photos

- **View**: Click the "View" button to see the full-size image in a new tab
- **Delete**: Click the "Delete" button to remove a photo (with confirmation)
- **Gallery**: All photos are displayed in a responsive grid with metadata

## ⚙️ Configuration

### File Size Limits

The default maximum file size is 16MB. You can modify this in `app.py`:

```python
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
```

### Supported File Types

Currently supports:
- PNG
- JPG/JPEG
- GIF
- WebP

You can modify the allowed extensions in `app.py`:

```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
```

### Security

- Files are saved with unique names to prevent conflicts
- File types are validated before upload
- Secure filename handling prevents path traversal attacks

## 🔧 Customization

### Changing the Theme

The color scheme can be modified in the CSS section of `templates/index.html`. Look for these CSS variables:

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Adding Features

The application is built with Flask and can be easily extended:

- Add user authentication
- Implement photo albums/categories
- Add image editing capabilities
- Integrate with cloud storage (AWS S3, Google Cloud Storage)
- Add social sharing features

## 🛠️ Development

### Running in Development Mode

The application runs in debug mode by default, which provides:
- Automatic reloading when code changes
- Detailed error messages
- Debug toolbar

### Production Deployment

For production deployment:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Configure proper security headers
4. Set up HTTPS
5. Use environment variables for sensitive configuration

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application!

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5002)
   ```

2. **Permission errors**: Make sure the `uploads` directory is writable

3. **File upload fails**: Check file size and format restrictions

4. **Images not displaying**: Verify the `uploads` directory exists and has proper permissions

### Getting Help

If you encounter any issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure you have proper file permissions
4. Check that the upload directory exists and is writable

---

**Enjoy uploading and sharing your photos! 📸✨** 