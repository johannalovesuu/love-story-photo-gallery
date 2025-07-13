from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import uuid
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Configuration
UPLOAD_FOLDER = 'uploads'
REVIEWS_FILE = 'restaurant_reviews.json'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_reviews():
    """Load restaurant reviews from JSON file"""
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_reviews(reviews):
    """Save restaurant reviews to JSON file"""
    with open(REVIEWS_FILE, 'w') as f:
        json.dump(reviews, f, indent=2)

def get_uploaded_photos():
    """Get list of uploaded photos with metadata"""
    photos = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if allowed_file(filename):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file_stats = os.stat(file_path)
                photos.append({
                    'filename': filename,
                    'size': file_stats.st_size,
                    'upload_time': datetime.fromtimestamp(file_stats.st_mtime)
                })
    return sorted(photos, key=lambda x: x['upload_time'], reverse=True)

@app.route('/')
def index():
    """Serve the main love story page"""
    return send_from_directory('.', 'loveyou.html')

@app.route('/test')
def test():
    """Serve the test upload page"""
    return send_from_directory('.', 'test_upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print(f"=== UPLOAD REQUEST ===")
    print(f"Upload request received. Files: {list(request.files.keys())}")
    
    if 'file' not in request.files:
        print("No 'file' key in request.files")
        return jsonify({'success': False, 'message': 'No file selected'})
    
    file = request.files['file']
    print(f"File received: {file.filename}, Content-Type: {file.content_type}")
    
    if file.filename == '':
        print("Empty filename")
        return jsonify({'success': False, 'message': 'No file selected'})
    
    if file and file.filename and allowed_file(file.filename):
        # Generate unique filename to prevent conflicts
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        print(f"Processing file: {original_filename} -> {unique_filename}")
        
        try:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Verify file was saved
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                print(f"✅ File saved successfully: {unique_filename}, size: {file_size} bytes")
                
                # Count total photos after upload
                total_photos = len(get_uploaded_photos())
                print(f"📸 Total photos in uploads folder: {total_photos}")
                
                return jsonify({
                    'success': True, 
                    'message': 'Photo uploaded successfully!',
                    'filename': unique_filename,
                    'url': url_for('uploaded_file', filename=unique_filename)
                })
            else:
                print(f"❌ File was not saved: {file_path}")
                return jsonify({'success': False, 'message': 'File was not saved properly'})
        except Exception as e:
            print(f"❌ Error saving file: {str(e)}")
            return jsonify({'success': False, 'message': f'Error uploading file: {str(e)}'})
    else:
        print(f"❌ Invalid file type: {file.filename}")
        return jsonify({'success': False, 'message': 'Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WebP files.'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/photos')
def get_photos():
    """API endpoint to get all uploaded photos"""
    photos = get_uploaded_photos()
    print(f"API /photos called - found {len(photos)} photos")
    for i, photo in enumerate(photos):
        print(f"  {i+1}. {photo['filename']} - {photo['upload_time']} - {photo['size']} bytes")
    
    result = [{
        'filename': photo['filename'],
        'url': url_for('uploaded_file', filename=photo['filename']),
        'upload_time': photo['upload_time'].strftime('%B %d, %Y'),
        'size': photo['size']
    } for photo in photos]
    
    print(f"Returning {len(result)} photos to client")
    return jsonify(result)

@app.route('/reviews')
def get_reviews():
    """API endpoint to get all restaurant reviews"""
    reviews = load_reviews()
    print(f"API /reviews called - found {len(reviews)} reviews")
    return jsonify(reviews)

@app.route('/add_review', methods=['POST'])
def add_review():
    """API endpoint to add a new restaurant review"""
    try:
        data = request.get_json()
        print(f"=== ADDING REVIEW ===")
        print(f"Review data: {data}")
        
        # Validate required fields
        required_fields = ['name', 'date', 'rating']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'})
        
        # Create review object
        review = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'date': data['date'],
            'cuisine': data.get('cuisine', ''),
            'rating': int(data['rating']),
            'johanna_favorite': data.get('johanna_favorite', ''),
            'joseph_favorite': data.get('joseph_favorite', ''),
            'review_text': data.get('review_text', ''),
            'created_at': datetime.now().isoformat()
        }
        
        # Load existing reviews and add new one
        reviews = load_reviews()
        reviews.insert(0, review)  # Add to beginning
        save_reviews(reviews)
        
        print(f"✅ Review added successfully: {review['name']}")
        print(f"📝 Total reviews: {len(reviews)}")
        
        return jsonify({'success': True, 'message': 'Review added successfully!', 'review': review})
        
    except Exception as e:
        print(f"❌ Error adding review: {str(e)}")
        return jsonify({'success': False, 'message': f'Error adding review: {str(e)}'})

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify({'success': True, 'message': 'Photo deleted successfully!'})
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error deleting file: {str(e)}'})
    else:
        return jsonify({'success': False, 'message': 'File not found'})

if __name__ == '__main__':
    # Use environment variable for port (for deployment)
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)