import os

# Robust Fragments for Scrubbing (Remove remnants of the 'Cash for Cars' and 'Solar' templates)
fragments_to_scrub = {
    'My truck broke down': 'We had some major fence damage',
    'needed it gone fast': 'needed it fixed fast',
    'towed it for free': 'repaired it professionally',
    'paid me cash same day': 'completed the work quickly',
    'Best prices with Cash for Cars': 'Best values with AV Handyman Pros',
    'Selling your car should be easy': 'Home repairs should be easy',
    'We tow any vehicle': 'We handle all repairs',
    'junk car': 'property damage',
    'free pickup': 'free estimates',
}

# Sub-Footer Correction (The brand transform missed this specific combined string)
global_replaces = {
    'Complete Home & Property Solutions in Palmdale, Lancaster & Quartz Hill': 'Complete Home & Property Solutions in Palmdale, Lancaster, and the Antelope Valley',
}

cities = {
    'palmdale': 'Palmdale',
    'lancaster': 'Lancaster',
    'quartz-hill': 'Quartz Hill',
    'leona-valley': 'Leona Valley',
    'acton': 'Acton',
    'rosamond': 'Rosamond',
    'littlerock': 'Littlerock',
    'lake-los-angeles': 'Lake Los Angeles'
}

def scrub_content(content):
    new_content = content
    for old, new in fragments_to_scrub.items():
        new_content = new_content.replace(old, new)
    for old, new in global_replaces.items():
        new_content = new_content.replace(old, new)
    return new_content

def localise_location_page(content, city_name):
    # Aggressively ensure the target city is correctly mentioned in key zones
    new_content = content
    
    # Replace any "Lancaster" mentions in Hero/Title/H1 if this is NOT the Lancaster page
    if city_name != 'Lancaster':
        new_content = new_content.replace('Lancaster, CA', f'{city_name}, CA')
        new_content = new_content.replace('residents in Lancaster', f'residents in {city_name}')
        new_content = new_content.replace('neighborhoods in Lancaster', f'neighborhoods in {city_name}')
        new_content = new_content.replace('Our Services in Lancaster', f'Our Services in {city_name}')
        new_content = new_content.replace('Lancaster Reviews', f'{city_name} Reviews')
        # Catch the local business name in JSON-LD if it's wrong
        new_content = new_content.replace('"name": "AV Handyman Pros in Lancaster"', f'"name": "AV Handyman Pros in {city_name}"')

    return new_content

def main():
    root_dir = '/Users/mediusa/NOVA/Repos/Handy Man Services'
    
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs: dirs.remove('.git')
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Fragment Scrub
                new_content = scrub_content(content)
                
                # 2. Location Alignment
                # Determine which city this corresponds to based on path
                for slug, display in cities.items():
                    if f'locations/{slug}' in file_path:
                        new_content = localise_location_page(new_content, display)
                        break
                
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {file_path}")

if __name__ == "__main__":
    main()
