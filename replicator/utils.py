def get_notify_data(payload):
    elements = payload.split(',')
    operation = ''
    keys, values, items = [], [], []
    email = ''
    for element in elements:
        key, value = element.split('=')
        if key == 'OPERATION':
            operation = value
        else:
            if operation == 'INSERT':
                keys.append(key)
                values.append(f"'{value}'")
            elif operation in ['UPDATE', 'DELETE']:
                if key == 'OLD_EMAIL':
                    email = value
                else:
                    items.append(f"{key}='{value}'")
    if operation == 'INSERT':
        keys_str = ', '.join(keys)
        values_str = ', '.join(values)
        data = (keys_str, values_str)
    elif operation in ['UPDATE', 'DELETE']:
        data = (email, ', '.join(items))
    return operation, data
