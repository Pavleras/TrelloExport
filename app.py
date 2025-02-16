import json

def list_first_card_details(json_file):
    # Cargar el archivo JSON
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Crear un diccionario para mapear IDs de Custom Fields con nombres
    custom_fields_map = {}
    if 'customFields' in data:
        for field in data['customFields']:
            custom_fields_map[field['id']] = field['name']
    
    # Crear un diccionario para mapear IDs de listas con nombres
    list_names = {}
    if 'lists' in data:
        for lst in data['lists']:
            list_names[lst['id']] = lst['name']
    
    # Verificar si hay tarjetas en el JSON
    if 'cards' in data and len(data['cards']) > 0:
        for card in data['cards']:
            list_id = card.get('idList', '')
            list_name = list_names.get(list_id, '')
            
            # Omitir tarjetas de listas no deseadas
            if list_name in ["INFORMACIÓN"]:
                continue
            if card.get('name') in ["PROCEDIMENTS"]:
                continue
            
            # Filtrar tarjetas que tienen al menos un campo personalizado con un valor asignado
            valid_custom_fields = [
                field for field in card.get('customFieldItems', [])
                if field.get('value')
            ]
            
            if valid_custom_fields:
                print("Detalles de la tarjeta:")
                print(f"  Nombre: {card.get('name', 'N/A')}")
                print(f"  Enlace: {card.get('url', 'N/A')}")
                
                # Extraer los custom fields con nombres reales
                print("  Campos personalizados:")
                for field in valid_custom_fields:
                    field_id = field.get('idCustomField', 'N/A')
                    field_name = custom_fields_map.get(field_id, field_id)  # Obtener el nombre real o dejar el ID si no está
                    field_value = field.get('value', {}).get('number', 'N/A')
                    print(f"    {field_name}: {field_value}")
    else:
        print("No se encontraron tarjetas en el JSON.")

# Nombre del archivo JSON exportado desde Trello
json_file = "trello_export.json"  # Reemplázalo con la ruta de tu archivo JSON

list_first_card_details(json_file)
