def format_person_info(data: dict) -> str:
    default_fields = ['email', 'address', 'phone']
    requested = data.get('requested_fields', default_fields)
    
    response = []
    for field in requested:
        value = data.get(field, 'Not available')
        response.append(f"- {field.capitalize()}: {value}")
    
    if 'source' in data:
        response.append(f"\nSource: {data['source']}")
    
    return "\n".join(response)