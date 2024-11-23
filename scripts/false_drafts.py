import os
import re

def check_drafts(directory):
    draft_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if re.search(r'^draft:\s*true$', content, re.MULTILINE):
                        draft_files.append(file_path)
    return draft_files

def update_drafts(directory):
    draft_files = check_drafts(directory)
    if draft_files:
        print("The following files are marked as drafts and will be updated:")
        for draft in draft_files:
            print(draft)
            with open(draft, 'r', encoding='utf-8') as f:
                content = f.read()
            updated_content = re.sub(r'^draft:\s*true$', 'draft: false', content, flags=re.MULTILINE)
            with open(draft, 'w', encoding='utf-8') as f:
                f.write(updated_content)
    else:
        print("No draft files found.")

if __name__ == "__main__":
    directory = 'content/post/2024/'
    update_drafts(directory)
