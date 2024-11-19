import os
from datetime import datetime
import shutil
from pathlib import Path

def find_matching_files(directory):
    """
    Find groups of files (txt, images, videos) that share the same base name.
    Returns a list of dictionaries containing file groups.
    """
    files = os.listdir(directory)
    file_groups = {}
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    video_extensions = {'.mp4', '.mov', '.avi'}
    
    for file in files:
        base_name = os.path.splitext(file)[0]
        ext = os.path.splitext(file)[1].lower()
        
        if base_name not in file_groups:
            file_groups[base_name] = {
                'base_name': base_name,
                'txt': None,
                'image': None,
                'video': None
            }
        
        if ext == '.txt':
            file_groups[base_name]['txt'] = file
        elif ext in image_extensions:
            file_groups[base_name]['image'] = file
        elif ext in video_extensions:
            file_groups[base_name]['video'] = file
    
    complete_groups = [group for group in file_groups.values() if group['txt'] is not None]
    return complete_groups

def create_hugo_post(group, source_dir, output_dir="content/post"):
    """
    Generate a Hugo markdown file for a group of related files.
    """
    try:
        # Create slug from base name
        title = group['base_name']
        slug = title.lower().replace(" ", "-")
        
        # Create post directory
        year = datetime.now().strftime("%Y")
        post_dir = os.path.join(output_dir, year, slug)
        os.makedirs(post_dir, exist_ok=True)
        
        # Read text content
        txt_path = os.path.join(source_dir, group['txt'])
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get first few words of content for description
        description = content.split('.')[0] if content else "Description goes here..."
        
        # Get image path for front matter
        image_path = ""
        if group['image']:
            image_path = group['image']
        
        # Prepare markdown content
        markdown_content = [
            "---",
            f'title: "{title}"',
            f"date: {datetime.now().strftime('%Y-%m-%d')}",
            f'description: "{description}"',
            'tags: [""]',
            f'image: "{image_path}"',
            "draft: true",
            "lightgallery: true",
            "---",
            "",
            content,
            ""
        ]
        
        # Add image if exists
        if group['image']:
            image_filename = group['image']
            # Copy image file
            shutil.copy2(
                os.path.join(source_dir, image_filename),
                os.path.join(post_dir, image_filename)
            )
            markdown_content.append(f"![{title}]({image_filename})")
            markdown_content.append("")
        
        # Add video if exists
        if group['video']:
            video_filename = group['video']
            # Copy video file
            shutil.copy2(
                os.path.join(source_dir, video_filename),
                os.path.join(post_dir, video_filename)
            )
            markdown_content.append(f"{{{{< video src=\"{video_filename}\" >}}}}")
            markdown_content.append("")
        
        # Write markdown file
        md_file = os.path.join(post_dir, "index.md")
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        print(f"Created post: {slug}")
        print(f"  - Title: {title}")
        print(f"  - Description: {description[:50]}...")  # Print first 50 chars of description
        return True
    
    except Exception as e:
        print(f"Error creating post for {title}: {str(e)}")
        return False

def main():
    # Get the project root directory
    project_root = os.getcwd()
    
    # Specify source directory (where your content files are)
    source_dir = os.path.join(project_root, "content", "post", "2024")
    
    # Find all matching file groups
    file_groups = find_matching_files(source_dir)
    
    if not file_groups:
        print("No matching file groups found. Each post needs at least a .txt file.")
        return
    
    print(f"Found {len(file_groups)} file groups to process...")
    print("-" * 50)
    
    # Create posts for each group
    successful = 0
    for group in file_groups:
        if create_hugo_post(group, source_dir):
            successful += 1
        print("-" * 50)
    
    print(f"\nProcessing complete! Created {successful} out of {len(file_groups)} possible posts.")

if __name__ == "__main__":
    main()