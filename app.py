import streamlit as st
import json
import pyperclip  # Necesario para copiar al portapapeles

def list_first_card_details(data):
    """
    data será el contenido JSON ya cargado en memoria (no un path de fichero).
    """
    custom_fields_map = {field['id']: field['name'] for field in data.get('customFields', [])}
    list_names = {lst['id']: lst['name'] for lst in data.get('lists', [])}

    results = []
    for card in data.get('cards', []):
        list_id = card.get('idList', '')
        list_name = list_names.get(list_id, '')

        if list_name in ["INFORMACIÓN"]:
            continue
        if card.get('name') in ["PROCEDIMENTS"]:
            continue

        valid_custom_fields = [field for field in card.get('customFieldItems', []) if field.get('value')]

        if valid_custom_fields:
            card_info = f"**Nombre**: {card.get('name', 'N/A')}\n"
            card_info += f"**Enlace**: {card.get('url', 'N/A')}\n"
            card_info += "Campos personalizados:\n"

            for field in valid_custom_fields:
                field_id = field.get('idCustomField', 'N/A')
                field_name = custom_fields_map.get(field_id, field_id)
                field_value = field.get('value', {}).get('number', 'N/A')
                card_info += f"  - {field_name}: {field_value}\n"

            results.append(card_info)

    return "\n\n".join(results) if results else "No se encontraron tarjetas en el JSON."

def main():
    st.title("Análisis de Cursos de Trello")
    st.write("Sube tu fichero JSON exportado para procesarlo.")

    uploaded_file = st.file_uploader("Selecciona el fichero JSON", type=["json"])

    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            results = list_first_card_details(data)

            st.subheader("Resultados")
            resultado_texto = results if results else "No hay datos procesados."
            
            # Mostrar el resultado en un cuadro de texto para copiar fácilmente
            text_area = st.text_area("Texto procesado", resultado_texto, height=300)
            
            # Botón para copiar al portapapeles
            if st.button("Copiar al portapapeles"):
                pyperclip.copy(resultado_texto)
                st.success("Texto copiado al portapapeles")

        except Exception as e:
            st.error(f"Error al procesar el JSON: {e}")

if __name__ == "__main__":
    main()
