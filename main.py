from nicegui import ui

lang_list = ['English', 'French', 'German', 'Spanish', 'Chinese', 'Japanese', 'Korean']

feedback_label = None
reply_avatar = 'https://api.dicebear.com/9.x/croodles-neutral/svg?seed=Chloe'

def generate_translation():

    global feedback_label
    input_text = text_input.value
    lang = lang_select.value

    if input_text and lang:
        message = f'Translating "{input_text}" to {lang}...'
        if feedback_label:
            feedback_label.text = message
        else:
           
            with reply_container:
                feedback_label = ui.chat_message(text = message, avatar = reply_avatar).classes('w-full')
                #feedback_label.style('background-color: #672733')
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
        reply_container = ui.column().classes('w-full')
        
# Start the NiceGUI app
ui.run()
