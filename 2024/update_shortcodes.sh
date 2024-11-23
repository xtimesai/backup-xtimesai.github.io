#!/bin/zsh

# Change to the directory where the posts are located
cd content/post/2024

# Loop through each directory
for dir in */; do
    # Check if there's an index.md file
    if [ -f "$dir/index.md" ]; then
        # Read the content of the file
        content=$(cat "$dir/index.md")
        
        # Replace the shortcode with the correct one or remove it if not needed
        updated_content=$(echo "$content" | sed 's/{{< shortcode-name >}}//g')
        
        # Rename index.md to folder name
        folder_name=$(basename "$dir")
        echo "$updated_content" > "$folder_name.md"
        
        # Delete the old directory
        rm -rf "$dir"
    fi
done

echo "All shortcodes have been updated or removed, files renamed, and old directories deleted."
