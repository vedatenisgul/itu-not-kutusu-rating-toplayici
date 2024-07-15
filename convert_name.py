import re

def convert_name(name):
    name = name.replace('  ', '-') 
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'Ç': 'C', 'Ğ': 'G', 'İ': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U',
        ' ': '-'
    }
    
    # Apply all replacements in one go
    for turkish_char, english_char in replacements.items():
        name = name.replace(turkish_char, english_char)

    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)  # Remove remaining unwanted characters
    
    return name