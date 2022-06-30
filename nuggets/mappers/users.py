def map_users(record):
    user=dict(record)
    user['id'] = str(user.get('id'))
    
    return user