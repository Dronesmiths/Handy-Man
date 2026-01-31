import os
import re

def standardize_favicons():
    root_dir = "."
    favicon_block = """    <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
    <link rel="apple-touch-icon" sizes="180x180" href="/images/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="/images/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/images/favicon-16x16.png">"""

    for root, dirs, files in os.walk(root_dir):
        if ".git" in dirs:
            dirs.remove(".git")
        if "scripts" in dirs:
            dirs.remove("scripts")
            
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Remove existing favicon/icon links
                # Matches: <link rel="icon" ... > or <link rel="apple-touch-icon" ... >
                content = re.sub(r'\s*<link rel="(icon|apple-touch-icon)"[^>]*>', '', content)
                
                # Insert the standardized block before </head>
                if "</head>" in content:
                    # Try to insert after the last meta tag or before </head>
                    if "    <link" in content:
                         # Insert before the first remaining link tag if any
                         content = content.replace("    <link", favicon_block + "\n    <link", 1)
                    else:
                         content = content.replace("</head>", favicon_block + "\n</head>", 1)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Processed: {file_path}")

if __name__ == "__main__":
    standardize_favicons()
