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

if __name__ == "__main__":
    directory = 'content/post/2024/'
    drafts = check_drafts(directory)
    if drafts:
        print("The following files are marked as drafts:")
        for draft in drafts:
            print(draft)
    else:
        print("No draft files found.")
