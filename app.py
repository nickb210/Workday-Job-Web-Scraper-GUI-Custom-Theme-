#!/usr/bin/env python3
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk 
from PIL import Image, ImageTk
from tkinter import filedialog
from ttkbootstrap import Style
from tkinter.filedialog import askopenfile
import subprocess, sys, time, os 
from threading import Thread
import pyperclip
from jobsSearch_dataFrame import job_search

STYLE_JSON = './themes/ttkbootstrap_themes.json'
class SplashScreen(tk.Toplevel):
    def __init__(self, container):
        tk.Toplevel.__init__(self, container)
        s = Style(
            theme='my_gui_theme_dark',
            themes_file=STYLE_JSON
            )
        
        self.title("Welcome")
        self.geometry("400x400")
        self.configure(bg="#1f262d")
        self.resizable(False, False)
        
        main_lbl = ttk.Label(self, text="Welcome", font=('Poppins ExtraLight', 48), style="custom.TLabel")
        main_lbl.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        self.progress_bar = ttk.Progressbar(self, orient=HORIZONTAL, length=300, mode='determinate')
        self.progress_bar.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        self.progress_value = tk.StringVar()
        
        self.change_label = ttk.Label(self, text="text", textvariable=self.progress_value, font=('Poppins ExtraLight', 10))
        self.change_label.place(x=50, y=135, anchor="nw")
        
    def progress(self):
        
        progressBarValue = self.progress_bar["value"]
        dots = int(progressBarValue) % 4
        
        if self.progress_bar["value"] < self.progress_bar["maximum"]:
            
            if self.progress_bar["value"] <= 33.0:
                self.progress_value.set("Loading . . .")
            
            elif self.progress_bar["value"] > 33.0 and self.progress_bar["value"] <= 66.0:
                self.progress_value.set("Initializing GUI . . .")
                
            else:
                self.progress_value.set("Starting Application . . .")
                
            self.progress_bar["value"] += 1
            self.after(50, self.progress)
            

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # remove main window for splash screen
        self.withdraw()

        splash = SplashScreen(self)
        splash.progress()

        # after 3 seconds remove splash screen window
        self.after(5000, splash.withdraw)

        # after 3 seconds show main window
        self.after(5000, self.deiconify)
        
        self.title("My GUI")
        self.geometry("800x566") # WIDTHxHEIGHT
        self.resizable(False, False)
        
        # input variabels for 'search' and 'company' selected from combobox
        self.search_query = StringVar()
        self.company_selection = StringVar()
        
        s = Style(theme='my_gui_theme_dark', themes_file=STYLE_JSON)
        s.configure('custom.TButton', font=('Poppins ExtraLight', 18), bg="#00b500")
        s.configure('my.custom.TButton', font=('Poppins ExtraLight', 10), background="#20272e", borderwidth=0)
        s.configure('custom.TLabel', fg="#aabac8")
        s.configure('custom.TRadiobutton', font=('SF Pro Rounded Thin', 14))
        s.configure('custom.TLabelFrame', bg="white")
        s.configure('custom.Horizontal.TProgressbar', background='#00de00', thickness=10)
        s.configure('Treeview.Heading', font=('SF Pro Rounded Thin', 12))
        
        self.frames = dict()
        
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for FrameClass in (page1, page2):
            frame = FrameClass(container, self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="NSEW")
            
        
        # show page 1 
        self.show_frame(page1)
        #self.show_frame(SplashScreen)
    
    def show_frame(self, container):
        frame = self.frames[container]
        frame_name = str(frame).split('!')[-1]
        
        #print(self.shared_data["company_selection"].get())
        if frame_name == "page2":
            page2.job_query(frame)
            pass
        
        frame.tkraise()
    
         
       
class page1(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        '''
        ===================================================================================================
        * Setup and configure UI widgets 
        =================================================================================================== 
        '''
       
        main_lbl = ttk.Label(self, text="Welcome", font=('Poppins ExtraLight', 48), style="custom.TLabel")
        main_lbl.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        
        search_label = ttk.Label(self, text="Search for:", font=('Poppins ExtraLight', 20))
        search_label.place(x=260, y=130)
        
        search_entry = Entry(self, font=('Poppins ExtraLight', 18), bd=0, width=25, textvariable=self.controller.search_query)
        search_entry.place(x=260, y=170)
        
        company_label = ttk.Label(self, text="Company:", font=('Poppins ExtraLight', 20), width=25)
        company_label.place(x=260, y=220)
        
        companies = ["Booz Allen Hamilton", "Trend Micro"]
        
        #company_combobox = ttk.Combobox(self, values=companies, font=('Poppins ExtraLight', 16), width=23, textvariable=self.controller.shared_data["company_selection"])
        company_combobox = ttk.Combobox(self, values=companies, font=('Poppins ExtraLight', 16), width=23, textvariable=self.controller.company_selection)
        company_combobox.place(x=260, y=260)
        
        img = tk.PhotoImage(file='./icons/arrow_right.png')
        search_button = ttk.Button(self, text="         Search      ", image=img, compound=tk.RIGHT, width=15, style='custom.TButton', command=lambda: controller.show_frame(page2))
        search_button.image = img
        search_button.place(x=300, y=330)
        
        # footer
        footer_text = "Version 1.0 | Made by @NickBrell"
        footer = tk.Label(self, text=footer_text, font=('Poppins ExtraLight', 14), fg="#aabac8", bg="#58427a", anchor="w")
        footer.pack(side="bottom", fill="x", ipadx=40)
    
        
        
class page2(ttk.Frame):
    def __init__(self, container, controller):
        super().__init__(container)
        self.controller = controller
        
        '''
        ===================================================================================================
        * Setup and configure UI widgets 
        =================================================================================================== 
        '''
        main_lbl = ttk.Label(self, text="RESULTS", font=('Poppins ExtraLight', 48), style="custom.TLabel")
        main_lbl.place(relx=0.5, rely=0.1, anchor=CENTER)
        
        tv_frame = tk.LabelFrame(self, text="Jobs", padx=10, pady=10, font=('Poppins ExtraLight', 20))
        tv_frame.place(width=700, height=300, x=50, y=120)
        
        #tv = ttk.Treeview(self)
        #tv.place(width=700, height=300, x=50, y=120)
        self.tv = ttk.Treeview(tv_frame)
        self.tv.place(relheight=1, relwidth=1)
        
        tv_scroll_x = tk.Scrollbar(tv_frame, orient="horizontal", command=self.tv.xview)
        tv_scroll_y = tk.Scrollbar(tv_frame, orient="vertical", command=self.tv.yview)
        self.tv.configure(xscrollcommand=tv_scroll_x.set, yscrollcommand=tv_scroll_y.set)
        
        # bind 'Double Clicking' to function selectItem()
        self.tv.bind("<Double-1>", self.selectItem)
        
        tv_scroll_x.pack(side="bottom", fill="x")
        tv_scroll_y.pack(side="right", fill="y")
        
        self.link = tk.StringVar()
        self.link_label = ttk.Label(self, text="text", textvariable=self.link, font=('Poppins ExtraLight', 9))
        self.link_label.place(x=25, y=430, anchor="nw")
        
        img = ImageTk.PhotoImage(file='./icons/arrow_left.png')
        back_button = ttk.Button(self, text="      Go Back         ", image=img, compound=tk.LEFT, width=15, style='custom.TButton', command=lambda: controller.show_frame(page1))
        back_button.image = img
        #back_button = ttk.Button(self, text="Go Back", width=15, style='custom.TButton', command=self.job_query)
        back_button.place(x=300, y=485)
        
        img_load = Image.open('./icons/help.png')
        img_help = ImageTk.PhotoImage(img_load)
        help_button = ttk.Button(self, image=img_help, compound=tk.CENTER, style='my.custom.TButton')
        
        help_button.image = img_help
        help_button.place(x=10, y=10)
        
        # footer
        footer_text= "Version 1.0 | Made by @NickBrell"
        footer = tk.Label(self, text=footer_text, font=('Poppins ExtraLight', 14), fg="#aabac8", bg="#58427a", anchor="w")
        footer.pack(side="bottom", fill="x", ipadx=40)
        
    
    def job_query(self):
        job_search_str     = self.controller.search_query.get()
        company_search_str = self.controller.company_selection.get()
        
        # run the job search using the string from 'job_search_str'
        search = job_search(job_search_str)
        
        self.tv["column"] = list(search.columns)
        self.tv["show"] = "headings"
        
        # set column names and widths
        for column in self.tv["columns"]:
            if column == 'url':
                self.tv.column(column, width=800)
                self.tv.heading(column, text="Link")
            if column == 'job_post_date':
                self.tv.column(column, width=125)
                self.tv.heading(column, text="Post Date")
            if column == 'job_location':
                self.tv.column(column, width=275)
                self.tv.heading(column, text="Location")
            if column == 'job_title':
                self.tv.column(column, width=250)
                self.tv.heading(column, text="Job")
        
        search_rows = search.to_numpy().tolist()
        
        # insert each row into TreeView
        # https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        for row in search_rows:
            self.tv.insert("", "end", values=row)
    
    # function returns link when double clicking on a row in the TreeView
    def selectItem(self, event):
        currentItem = self.tv.item(self.tv.focus())
        column      = self.tv.identify('item', event.x, event.y)
        
        # get the job name and job URL
        job  = currentItem['values'][0]
        link = currentItem['values'][-1]
        
        self.link.set(f"Copied '{job}' to clipboard!\nLink:\n{link}")
        pyperclip.copy(link)

root = App()
root.mainloop()