import pandas as pd
import cv2 #pip install opencv-python
import easyocr
import dearpygui.dearpygui as dpg #pip install dearpygui

Langs = ['en','ru']
selected_file = None
selected_lang = 'en' #set as default to find eng

dpg.create_context()

def callback(sender, data): #OK button
    global selected_file
    selected_file = str(data['selections'])
    index = selected_file.find("\': '")
    selected_file = selected_file[index+4:-2]    
    dpg.set_value("selected", ("Selected file: " + selected_file))

def selectLanguage(seder):
    val = dpg.get_value(seder)
    global selected_lang
    selected_lang = val

with dpg.file_dialog(directory_selector=False, height=300, width=600, show=False, callback=callback, tag="file_dialog_id", file_count=1):
    dpg.add_file_extension(".*")

with dpg.window(label="TextReader", width=800, height=450, tag="primary"):
    dpg.add_button(label="File selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.add_text(tag="selected", default_value="Selected path: None")
    dpg.add_listbox(tag="LangSelector", items=Langs, num_items=2, callback=selectLanguage)
    dpg.add_button(label="Convert to text", callback=lambda: proc(selected_file, selected_lang))
    dpg.add_text(tag="ans")

def proc(path, language):
    if(path == None): 
        dpg.set_value("ans", "File is not selected!")
        return
    dpg.set_value("ans", "Converting image to a text...")    
    img = cv2.imread(path)    
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    except: dpg.set_value("ans", "Error! Selected type is not an image.")
    noise = cv2.medianBlur(gray, 5)

    thresh = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    reader = easyocr.Reader([language])
    result = reader.readtext(gray)
    TextFromImg = (pd.DataFrame(result))[1]
    str_res = ''
    for i in TextFromImg:
        str_res += str(i) + '\n'
    dpg.set_value("ans", str_res)

dpg.create_viewport(title='Window1', height=450, width=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary", True)
dpg.start_dearpygui()
dpg.destroy_context()