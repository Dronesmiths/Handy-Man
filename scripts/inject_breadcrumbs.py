import os
import json

BASE_URL = "https://www.d1sxjpzrvgytjj.cloudfront.net"

def get_breadcrumbs(file_path, root_dir):
    relative_path = os.path.relpath(file_path, root_dir)
    parts = relative_path.split(os.sep)
    
    # Remove 'index.html' if it's the last part
    if parts[-1] == 'index.html':
        parts = parts[:-1]
    
    breadcrumbs = []
    
    # Always start with Home
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
        
        # Custom naming for known paths
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

def inject_breadcrumbs(file_path, root_dir):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if breadcrumb schema already exists
    if '"@type": "BreadcrumbList"' in content:
        return

    breadcrumbs = get_breadcrumbs(file_path, root_dir)
    
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbs
    }
    
    schema_script = f'\n    <script type="application/ld+json">\n    {json.dumps(breadcrumb_schema, indent=2)}\n    </script>'
    
    # Inject before the end of </head>
    if '</head>' in content:
        new_content = content.replace('</head>', f'{schema_script}\n\n</head>')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Injected Breadcrumbs: {file_path}")

def main():
    root_dir = '/Users/mediusa/NOVA/Repos/Handy Man Services'
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs: dirs.remove('.git')
        if 'scripts' in dirs: dirs.remove('scripts')
        for file in files:
            if file.endswith('.html'):
                inject_breadcrumbs(os.path.join(root, file), root_dir)

if __name__ == "__main__":
    main()
