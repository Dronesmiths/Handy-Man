import os

replacements = {
    '[BUSINESS_NAME]': 'AV Handyman Pros',
    '[REGION]': 'Antelope Valley, CA',
    '[PHONE_NUMBER]': '(661) 498-4444',
    '[PHONE_NUMBER_RAW]': '6614984444',
    '[CITY_HQ]': 'Palmdale',
    '[CITY_1]': 'Lancaster',
    '[CITY_2]': 'Quartz Hill',
    '[CITY_3]': 'Leona Valley',
    '[CITY_4]': 'Acton',
    '[CITY_5]': 'Rosamond',
    '[EMAIL_ADDRESS]': 'info@avhandymanpros.com',
    '[HERO_TITLE]': 'Complete Home & Property Solutions',
    '[HERO_DESCRIPTION]': 'Professional handyman, hauling, and landscape services in the Antelope Valley. From deck repairs to yard cleanup to custom patios - we do it all. Free estimates, quality work, trusted results.',
    '[SERVICE_4_TITLE]': 'Fence Repair',
    '[SERVICE_4_DESC]': 'Wood, vinyl, and gate repairs to restore safety and curb appeal.',
    '[SERVICE_5_TITLE]': 'Drywall Repair',
    '[SERVICE_5_DESC]': 'Hole patches, cracks, water damage fixes, and paint-ready finishes.',
    '[SERVICE_6_TITLE]': 'Small Remodel Projects',
    '[SERVICE_6_DESC]': 'Minor kitchen, bathroom, and interior upgrade projects without contractor pricing.',
    '[LICENSE_TEXT]': 'Licensed & insured for general handyman services.',
    '[GOOGLE_MAPS_URL]': 'https://maps.google.com/?q=Palmdale+CA',
    '[SUB_SERVICE_1]': 'Fence Repair',
    '[SUB_SERVICE_2]': 'Drywall Repair',
    '[SUB_SERVICE_3]': 'Small Remodel Projects',
    '[SUB_SERVICE_4]': 'Deck Repair',
    '[SUB_SERVICE_5]': 'Home Maintenance',
    '[FONT_HEADING]': 'Poppins',
    '[FONT_BODY]': 'Inter',
}

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for placeholder, value in replacements.items():
        new_content = new_content.replace(placeholder, value)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {file_path}")

def main():
    root_dir = '/Users/mediusa/NOVA/Repos/Handy Man Services'
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.html') or file.endswith('.js') or file.endswith('.json') or file.endswith('.css'):
                process_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
