import os
import re
import subprocess

# Configuration
base_dir = "/Users/mediusa/NOVA/Repos/Handy Man Services"
images_dir = os.path.join(base_dir, "images")
extensions_to_convert = (".png", ".jpg", ".jpeg")

# Mapping of original names to kebab-case
# (Adding explicit mappings for complex names to avoid collision or confusion)
name_mapping = {
    "Aged and broken backyard fence.png": "backyard-fence-broken.webp",
    "Clean and cleared backyard space.png": "backyard-space-clean.webp",
    "Cluttered backyard of discarded items.png": "backyard-cluttered.webp",
    "Freshly repaired wooden fence in sunlight.png": "fence-repaired.webp",
    "Rustic backyard oasis in Leona Valley.png": "leona-valley-oasis.webp",
    "fence-repair-pro.png": "fence-repair-pro.webp",
    "handyman-hero.png": "handyman-hero.webp",
    "handyman_deck_fence_repair.png": "handyman-deck-fence.webp",
    "handyman_home_maintenance.png": "handyman-maintenance.webp",
    "handyman_light_fixtures.png": "handyman-fixtures.webp",
    "handyman_painting_drywall.png": "handyman-painting.webp",
    "hauling_construction_debris.png": "hauling-debris.webp",
    "hauling_estate_cleanout.png": "hauling-estate.webp",
    "hauling_trash_junk.png": "hauling-junk.webp",
    "hauling_yard_waste.png": "hauling-yard.webp",
    "hero-pergola.png": "hero-pergola.webp",
    "landscape-hero.png": "landscape-hero.webp",
    "landscape_custom_patio.png": "landscape-patio.webp",
    "landscape_irrigation_system.png": "landscape-irrigation.webp",
    "landscape_outdoor_lighting.png": "landscape-lighting.webp",
    "landscape_retaining_wall.png": "landscape-wall.webp",
    "logo-full.png": "logo-placeholder.png",
    "logo.png": "logo.webp",
    "outdoor-lighting-pro.png": "outdoor-lighting-pro.webp",
    "professional_handyman_team_reed_and_sons_refined.png": "handyman-team-refined.webp",
    "professional_home_service_team_reed_and_sons_1769565297601.png": "home-service-team.webp",
    "residential-paving.png": "residential-paving.webp",
    "retaining-walls-pro.png": "retaining-walls-pro.webp",
    "waste-cleanup-pro.png": "waste-cleanup-pro.webp",
    "apple-touch-icon.png": "apple-touch-icon.png", # Keep name but convert? Actually apple prefers png.
    "favicon-16x16.png": "favicon-16x16.png",
    "favicon-32x32.png": "favicon-32x32.png",
}

def convert_to_webp(src, dest):
    print(f"Converting {src} -> {dest}")
    subprocess.run(["cwebp", "-q", "80", src, "-o", dest], check=True)

def update_references(old_name, new_name):
    print(f"Updating references: {old_name} -> {new_name}")
    # Escape special characters for regex
    escaped_old = re.escape(old_name)
    # We want to match exactly the filename, possibly preceded by path separators
    # and possibly followed by quotes or other delimiters.
    pattern = f"(?i){escaped_old}"
    
    for root, dirs, files in os.walk(base_dir):
        if ".git" in root: continue
        for file in files:
            if file.endswith((".html", ".css", ".js")):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = re.sub(pattern, new_name, content)
                
                if content != new_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"  Updated {filepath}")

def main():
    # 1. Convert and update mappings
    for old_name, new_name in name_mapping.items():
        old_path = os.path.join(images_dir, old_name)
        new_path = os.path.join(images_dir, new_name)
        
        if os.path.exists(old_path):
            if new_name.endswith(".webp"):
                convert_to_webp(old_path, new_path)
            # 2. Update references sitewide
            update_references(old_name, new_name)
        else:
            print(f"Skipping {old_name} (not found)")

    # Special case: catch any remaining .png, .jpg, .jpeg in js/html/css that we might have missed
    # (Optional, but let's stick to explicit mappings first for safety)

if __name__ == "__main__":
    main()
