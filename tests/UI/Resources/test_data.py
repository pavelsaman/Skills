

skills_valid = {
    'Scripting': 'Python',
    'Networking': 'flask'
}
skills_invalid = ['\'', '@', 'flask?', 'flaskflaskflaskflaskflaskflaska']
categories_valid = ['Scripting', 'Networking']

import os
facebook_valid_email = os.environ.get('FB_EMAIL'); 
facebook_valid_pwd = os.environ.get('FB_PWD');
