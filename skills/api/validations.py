from skills import Config


def validate_skill_json(data):
    if 'skill_name' not in data or 'category_name' not in data:
        return False
    if 'is_shown' not in data and len(data.keys()) != 2:
        return False
    if 'is_shown' in data and len(data.keys()) != 3:
        return False
    elif 'is_shown' in data and len(data.keys()) == 3 and not isinstance(data['is_shown'], bool):
        return False
    return True


def validate_category_json(data):
    if 'category_name' not in data:
        return False
    if 'is_shown' not in data and len(data.keys()) != 1:
        return False
    if 'is_shown' in data and len(data.keys()) != 2:
        return False
    elif 'is_shown' in data and len(data.keys()) == 2 and not isinstance(data['is_shown'], bool):
        return False
    return True


def validate_new_skill_name(skill_name):
    if not isinstance(skill_name, str):
        return False
    if len(skill_name) < Config.MIN_SKILL_LENGTH or len(skill_name) > Config.MAX_SKILL_LENGTH:
        return False
    for c in skill_name:
        if c in Config.FORBIDDEN_CHARACTERS:
            return False
    return True


def validate_new_category_name(category_name):
    if not isinstance(category_name, str):
        return False
    if len(category_name) < Config.MIN_CATEGORY_LENGTH or len(category_name) > Config.MAX_CATEGORY_LENGTH:
        return False
    for c in category_name:
        if c in Config.FORBIDDEN_CHARACTERS:
            return False
    return True
