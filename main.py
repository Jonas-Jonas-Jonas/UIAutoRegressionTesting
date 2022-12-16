#################################################################################################
# User Interface Code
# QA Toolkit - Version 1.0.0
#
# Important documentation for the UI - https://github.com/TomSchimansky/CustomTkinter/wiki
####################################################################################################

import tkinter
import customtkinter
from pathlib import Path
from tkinter import messagebox
import sys
import os



customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"


# ----------------------------------------------------------------------------------------------------------------

def correctpath():
    pathQA = 'C:/QA-Automated-Testing/'
    isExist = os.path.exists(pathQA)

    if isExist == 0:
        messagebox.showerror("ERROR: WRONG DIRECTORY", "Please install 'QA-Automated-Testing' into the C:\ folder. Program will now exit!")
        sys.exit()

#correctpath()

# ---------------------------------------------------------------------------------------------------------------


app = customtkinter.CTk()
app.geometry("600x500")
app.title("QA - Internal automated ProTouch UI regression Testing toolkit")


def button_callback():
    print("Button click")
    a = int(loop_times.get())
    print(a)
    
    

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)


label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT, text="Please select testing scenario")
label_1.pack(pady=12, padx=10)

# ------------------------------------ TEST SCENARIONS BELLOW ---------------------------------------------------------------------------


checkbox_1 = customtkinter.CTkCheckBox(master=frame_1, text='Terminal (Integrert) normal test')
checkbox_1.pack(pady=12, padx=10)


checkbox_2 = customtkinter.CTkCheckBox(master=frame_1, text='Terminal (Integrert) - Normal Table')
checkbox_2.pack(pady=12, padx=10)

checkbox_3 = customtkinter.CTkCheckBox(master=frame_1, text='Terminal (Integrert) - Combo')
checkbox_3.pack(pady=12, padx=10)

checkbox_4 = customtkinter.CTkCheckBox(master=frame_1, text='Terminal (Integrert) - Split Products')
checkbox_4.pack(pady=12, padx=10)

checkbox_5 = customtkinter.CTkCheckBox(master=frame_1, text='Terminal (Integrert) - placeholder')
checkbox_5.pack(pady=12, padx=10)


# ---------------------------------------------------------------------------------------------------------------

loop_times = customtkinter.CTkEntry(master=frame_1, placeholder_text="loop time")
loop_times.pack(pady=12, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text="Run selected tests")
button_1.pack(pady=12, padx=10)




app.resizable(width=False, height=False)
app.mainloop()

