
from nicegui import ui
import requests
import json
import base64

lang_list = ['afrikaans', 'amharic', 'arabic', 'bulgarian', 'bosnian', 'catalan', 
       'chinese (simplified)', 'czech', 'danish', 'dutch', 'english', 'finnish', 
       'french', 'german', 'greek', 'gujarati', 
       'hebrew', 'hindi', 'hungarian', 'icelandic', 
       'indonesian', 'italian', 'japanese',
       'javanese', 'kannada', 'korean', 'latin', 
       'latvian', 'lithuanian', 'malay', 'malayalam',
       'marathi', 'myanmar', 'nepali', 'norwegian', 
       'polish', 'portuguese', 'punjabi', 'romanian',
       'russian', 'serbian', 'sinhala', 'swedish', 
       'tamil', 'telugu', 'thai', 'turkish', 'ukrainian',
       'urdu', 'vietnamese' ]

feedback_label = None
reply_avatar = 'https://api.dicebear.com/9.x/croodles-neutral/svg?seed=Chloe'
phoneme_url = 'https://translator-sharmilathippa1.replit.app/translate_to_phoneme'
audio_response_url = 'https://translator-sharmilathippa1.replit.app/translate_to_audio'
output_file_path = 'output.mp3'

def save_audio_file(input_text, lang):
    try:
        audio_response = requests.post(audio_response_url, json={'input_text': input_text, 'target_language': lang})

        if audio_response.status_code == 200 and audio_response.headers.get('Content-Type') == 'audio/mpeg':
            with open(output_file_path, 'wb') as audio_file:
                for chunk in audio_response.iter_content(chunk_size=8192):
                    audio_file.write(chunk)
            print(f"Audio file saved succesfully at {output_file_path}")
            return True
        else:
            print(f"Failed to retrieve audio. Status Code: {audio_response.status_code}")
            print("Response content type:", audio_response.headers.get('Content-Type'))
            print("Response content:", audio_response.text)
            ui.notify(f"Failed to retrieve audio. Status Code: {audio_response.status_code}", color='red')
            return False
    except Exception as e:
        print("Error occurred while saving audio file:", e)
        ui.notify("Error occurred while saving audio file", color='red')
        return False

def generate_translation():

    input_text = text_input.value
    lang = lang_select.value

    if input_text and lang:
        
        reply_container.clear()
        try:
            phoneme_response = requests.post(phoneme_url, json={'input_text': input_text, 'target_language': lang})
            #audio_response = requests.post(audio_response_url, json={'input_text': input_text, 'target_language': lang})
        except requests.RequestException as e:
            ui.notify(f"Error: {e}", position='top-right', color='red')
            return
            
        with reply_container:
            if phoneme_response.status_code == 200:
                try:
                    phoneme = phoneme_response.json()

                    """
                    # Safely handle JSON parsing for audio response
                    if audio_response.headers.get('Content-Type') == 'audio/mpeg':
                        audio_output = audio_response.content
                        
                        audio_base64 = base64.b64encode(audio_output).decode('utf-8')
                        audio_url = f"data:audio/mpeg;base64,{audio_base64}"
                    """
                    # Display the transliterated text
                    transliterated_text = phoneme.get('transliterated_text', 'No transliterated text found.')
                    ui.chat_message(text=transliterated_text, avatar=reply_avatar).classes('w-full')
                    if save_audio_file(input_text, lang):
                        print("here!")
                        ui.audio(src = output_file_path, autoplay=True)
                    """
                        # If audio_url exists, display the audio player
                        if audio_url:
                            ui.audio(audio_url).classes('w-full')
                        else:
                            ui.notify('Audio URL not found in the response.', color='warning')
                    else:
                        ui.notify('Received non-JSON response for audio.', color='red')
                         print('Audio Response Type:', audio_response.headers.get('Content-Type'))
                    """
                except ValueError as e:
                        # Handle JSON decoding errors
                        ui.notify('Error parsing JSON response from the API.', color='red')
                        print(f'JSONDecodeError: {e}')
                        print('Phoneme Response Text:', phoneme_response.text)
                        print('Audio Response Text:', audio_response.text)
            else:
                    # Handle non-200 status codes
                    error_message = f"Phoneme API Error: {phoneme_response.status_code}, Audio API Error: {audio_response.status_code}"
                    ui.notify(error_message, color='red')
                    print("Phoneme Response Status Code:", phoneme_response.status_code)
                    print("Audio Response Status Code:", audio_response.status_code)
    else:
        ui.notify('Please enter text and select a language.', color = 'red')

# Create the header with navigation
with ui.header().style('background-color: #FFFFFF').classes('justify-center w-full'):
    ui.label('globalese').classes('text-4xl font-sans text-gray-800')
    ui.separator()
    
# Create the main content area
with ui.row().classes("w-full justify-center"):
    with ui.card().classes('w-1/2'):
        with ui.column().classes('w-full'):            
            text_input = ui.input(label = 'Enter text to translate').classes('w-full')
            ui.space()
            lang_select = ui.select(lang_list, label = 'Select language').classes('w-full')
            ui.space()
            with ui.row().classes('w-full justify-center'):
                ui.button('Generate Translation', on_click=generate_translation)
        ui.space()
        with ui.card().classes('w-full'):
            reply_container = ui.column().classes('w-full')
        
# Start the NiceGUI app
ui.run()
