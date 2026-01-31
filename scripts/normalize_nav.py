import os
import re

def normalize_nav(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    nav_pattern = re.compile(r'<nav class="nav-menu">\s*<ul>.*?</ul>\s*</nav>', re.DOTALL)
    
    active_link = ""
    if 'blog/' in file_path: active_link = "blog"
    elif 'services/' in file_path: active_link = "services"
    elif 'about/' in file_path: active_link = "about"
    elif 'contact/' in file_path: active_link = "contact"
    elif file_path.endswith('index.html') and os.path.dirname(file_path).endswith('Handy Man Services'):
        active_link = "home"
    
    def get_class(link_name):
        return ' class="active"' if active_link == link_name else ''

    new_nav = f'''<nav class="nav-menu">
                <ul>
                    <li><a href="/"{get_class("home")}>Home</a></li>
                    <li><a href="/services/"{get_class("services")}>Services</a></li>
                    <li><a href="/about/"{get_class("about")}>About Us</a></li>
                    <li><a href="/blog/"{get_class("blog")}>Blog</a></li>
                    <li><a href="/contact/"{get_class("contact")}>Contact</a></li>
                </ul>
            </nav>'''
            
    new_content = nav_pattern.sub(new_nav, content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Standardized Nav: {file_path}")

def main():
    root_dir = '/Users/mediusa/NOVA/Repos/Handy Man Services'
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs: dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                normalize_nav(os.path.join(root, file))

if __name__ == "__main__":
    main()
