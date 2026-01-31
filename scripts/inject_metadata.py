import os
import json
import re

BASE_URL = "https://d1aeo7n5mwkhsx.cloudfront.net"

def get_breadcrumbs(file_path, root_dir):
    relative_path = os.path.relpath(file_path, root_dir)
    parts = relative_path.split(os.sep)
    
    if parts[-1] == 'index.html':
        parts = parts[:-1]
    
    breadcrumbs = []
    breadcrumbs.append({
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": BASE_URL + "/"
    })
    
    current_path = ""
    for i, part in enumerate(parts):
        current_path += f"/{part}"
        name = part.replace('-', ' ').title()
        
        if part == 'services': name = 'Our Services'
        elif part == 'blog': name = 'Blog'
        elif part == 'about': name = 'About Us'
        elif part == 'contact': name = 'Contact'
        elif part == 'locations': name = 'Service Areas'
        
        breadcrumbs.append({
            "@type": "ListItem",
            "position": i + 2,
            "name": name,
            "item": f"{BASE_URL}{current_path}/"
        })
    
    return breadcrumbs

def inject_metadata(file_path, root_dir):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Calculate canonical URL
    relative_path = os.path.relpath(file_path, root_dir)
    path_parts = relative_path.split(os.sep)
    if path_parts[-1] == 'index.html':
        path_parts = path_parts[:-1]
    canonical_url = BASE_URL + "/" + ("/".join(path_parts) + "/" if path_parts else "")
    
    # 1. Handle Canonical Tag
    canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
    if '<link rel="canonical"' in content:
        content = re.sub(r'<link rel="canonical" href="[^"]*">', canonical_tag, content)
    else:
        content = content.replace('</head>', f'    {canonical_tag}\n</head>')

    # 2. Handle Breadcrumb Schema
    breadcrumbs = get_breadcrumbs(file_path, root_dir)
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbs
    }
    schema_script = f'<script type="application/ld+json">\n    {json.dumps(breadcrumb_schema, indent=2)}\n    </script>'
    
    # Check if breadcrumb schema already exists and replace it, or inject new
    if '"@type": "BreadcrumbList"' in content:
        # Complex replacement: find the script block containing BreadcrumbList
        # This is easier: just look for the pattern and replace it
        content = re.sub(r'<script type="application/ld\+json">.*?"@type":\s*"BreadcrumbList".*?</script>', schema_script, content, flags=re.DOTALL)
    else:
        content = content.replace('</head>', f'    {schema_script}\n</head>')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed: {file_path}")

def main():
    root_dir = '/Users/mediusa/NOVA/Repos/Handy Man Services'
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs: dirs.remove('.git')
        if 'scripts' in dirs: dirs.remove('scripts')
        for file in files:
            if file.endswith('.html'):
                inject_metadata(os.path.join(root, file), root_dir)

if __name__ == "__main__":
    main()
