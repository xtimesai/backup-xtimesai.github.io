# app.py
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flashing messages

# Configure upload folder
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {
    'txt': ['.txt'],
    'image': ['.jpg', '.jpeg', '.png', '.gif'],
    'video': ['.mp4', '.mov', '.avi']
}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename, file_type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in [ext[1:] for ext in ALLOWED_EXTENSIONS[file_type]]

def create_hugo_post(title, txt_path, image_path, video_path, output_dir):
    try:
        # Create slug from title
        slug = title.lower().replace(" ", "-")
        
        # Create post directory
        year = datetime.now().strftime("%Y")
        post_dir = os.path.join(output_dir, year, slug)
        os.makedirs(post_dir, exist_ok=True)
        
        # Read text content
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get first sentence for description
        description = content.split('.')[0] if content else "Description goes here..."
        
        # Get image filename for front matter
        image_filename = os.path.basename(image_path) if image_path else ""
        
        # Prepare markdown content
        markdown_content = [
            "---",
            f'title: "{title}"',
            f"date: {datetime.now().strftime('%Y-%m-%d')}",
            f'description: "{description}"',
            'tags: [""]',
            f'image: "{image_filename}"',
            "draft: true",
            "lightgallery: true",
            "---",
            "",
            content,
            ""
        ]
        
        # Add image if exists
        if image_path:
            image_filename = os.path.basename(image_path)
            shutil.copy2(image_path, os.path.join(post_dir, image_filename))
            markdown_content.append(f"![{title}]({image_filename})")
            markdown_content.append("")
        
        # Add video if exists
        if video_path:
            video_filename = os.path.basename(video_path)
            shutil.copy2(video_path, os.path.join(post_dir, video_filename))
            markdown_content.append(f"{{{{< video src=\"{video_filename}\" >}}}}")
            markdown_content.append("")
        
        # Write markdown file
        md_file = os.path.join(post_dir, "index.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        return True, f"Successfully created post at {md_file}"
        
    except Exception as e:
        return False, str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if any file was submitted
        if 'txt_file' not in request.files:
            flash('No text file selected')
            return redirect(request.url)
        
        txt_file = request.files['txt_file']
        image_file = request.files['image_file']
        video_file = request.files['video_file']
        title = request.form['title']
        output_dir = request.form['output_dir']
        
        # Validate required fields
        if not txt_file or txt_file.filename == '':
            flash('Text file is required')
            return redirect(request.url)
        
        if not title:
            flash('Title is required')
            return redirect(request.url)
            
        if not output_dir:
            flash('Output directory is required')
            return redirect(request.url)
        
        # Validate file types
        if not allowed_file(txt_file.filename, 'txt'):
            flash('Invalid text file format')
            return redirect(request.url)
        
        if image_file and image_file.filename and not allowed_file(image_file.filename, 'image'):
            flash('Invalid image file format')
            return redirect(request.url)
            
        if video_file and video_file.filename and not allowed_file(video_file.filename, 'video'):
            flash('Invalid video file format')
            return redirect(request.url)
        
        # Save files temporarily
        txt_path = os.path.join(UPLOAD_FOLDER, secure_filename(txt_file.filename))
        txt_file.save(txt_path)
        
        image_path = None
        if image_file and image_file.filename:
            image_path = os.path.join(UPLOAD_FOLDER, secure_filename(image_file.filename))
            image_file.save(image_path)
            
        video_path = None
        if video_file and video_file.filename:
            video_path = os.path.join(UPLOAD_FOLDER, secure_filename(video_file.filename))
            video_file.save(video_path)
        
        # Create post
        success, message = create_hugo_post(title, txt_path, image_path, video_path, output_dir)
        
        # Clean up temporary files
        if os.path.exists(txt_path):
            os.remove(txt_path)
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        if video_path and os.path.exists(video_path):
            os.remove(video_path)
        
        if success:
            flash(f'Success! {message}', 'success')
        else:
            flash(f'Error: {message}', 'error')
            
        return redirect(url_for('index'))
    
    return render_template('index.html')