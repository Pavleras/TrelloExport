import streamlit as st
import json

def list_first_card_details(data):
    """
    data será el contenido JSON ya cargado en memoria (no un path de fichero).
    """
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
        # Vamos a acumular resultados en un texto o una lista
        results = []
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
                # Construimos una representación de la info
                card_info = f"**Nombre**: {card.get('name', 'N/A')}\n"
                card_info += f"**Enlace**: {card.get('url', 'N/A')}\n"
                card_info += "Campos personalizados:\n"

                for field in valid_custom_fields:
                    field_id = field.get('idCustomField', 'N/A')
                    field_name = custom_fields_map.get(field_id, field_id)
                    field_value = field.get('value', {}).get('number', 'N/A')
                    card_info += f"  - {field_name}: {field_value}\n"

                results.append(card_info)

        return results
    else:
        return ["No se encontraron tarjetas en el JSON."]

def main():
    st.title("Filtrador de export de Trello")
    st.write("Sube tu fichero JSON exportado de Trello para procesarlo.")

    # Subida de fichero JSON con st.file_uploader
    uploaded_file = st.file_uploader("Selecciona el fichero JSON", type=["json"])

    if uploaded_file is not None:
        try:
            # Cargamos el contenido JSON
            data = json.load(uploaded_file)

            # Llamamos a la función para filtrar y procesar
            results = list_first_card_details(data)

            # Mostramos los resultados en Streamlit
            st.subheader("Resultados")
            for r in results:
                st.markdown(r)
                st.markdown("---")

        except Exception as e:
            st.error(f"Error al procesar el JSON: {e}")

if __name__ == "__main__":
    main()
