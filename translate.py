import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from googletrans import Translator, LANGUAGES
import os
import webbrowser

class UniversalTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal File Translator")
        self.root.geometry("800x500")
        
        self.translator = Translator()
        self.languages = LANGUAGES
        self.default_font = ('Arial', 10)
        
        # Variabili di stato
        self.input_path = ""
        self.output_dir = ""
        self.input_extension = ""
        
        # Variabili per controlli grafici
        self.input_file_var = tk.StringVar()
        self.output_name_var = tk.StringVar()
        self.src_lang_var = tk.StringVar(value='auto')
        self.dest_lang_var = tk.StringVar(value='italian')
        
        self.init_ui()
        self.setup_bindings()
        
    def init_ui(self):
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Sezione file di input
        ttk.Label(main_frame, text="Source file:", font=self.default_font).grid(row=0, column=0, sticky='w')
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        ttk.Label(input_frame, textvariable=self.input_file_var, width=60, relief="sunken", padding=5).pack(side='left', fill='x', expand=True)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input).pack(side='left', padx=5)
        
        # Sezione di selezione della lingua
        lang_frame = ttk.Frame(main_frame)
        lang_frame.grid(row=2, column=0, columnspan=2, pady=15, sticky='ew')
        ttk.Label(lang_frame, text="Source language:", font=self.default_font).grid(row=0, column=0, sticky='w')
        self.src_combo = ttk.Combobox(lang_frame, textvariable=self.src_lang_var, 
                                      values=['auto'] + sorted(self.languages.values(), key=lambda x: x.lower()), 
                                      state='readonly', width=25)
        self.src_combo.grid(row=1, column=0, padx=5, sticky='w')
        ttk.Label(lang_frame, text="Target language:", font=self.default_font).grid(row=0, column=1, sticky='w')
        self.dest_combo = ttk.Combobox(lang_frame, textvariable=self.dest_lang_var, 
                                       values=sorted(self.languages.values(), key=lambda x: x.lower()), 
                                       state='readonly', width=25)
        self.dest_combo.grid(row=1, column=1, padx=5, sticky='w')
        
        # Sezione output
        ttk.Label(main_frame, text="Output file name (without extension):", font=self.default_font).grid(row=3, column=0, sticky='w', pady=10)
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=0, columnspan=2, sticky='ew')
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_name_var, width=50)
        self.output_entry.pack(side='left', fill='x', expand=True)
        btn_frame = ttk.Frame(output_frame)
        btn_frame.pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Folder...", command=self.browse_output_dir).pack(side='left')
        ttk.Button(btn_frame, text="Copy Directory", command=self.copy_output_dir).pack(side='left', padx=5)
        
        # Anteprima del percorso completo
        ttk.Label(main_frame, text="Full path:", font=self.default_font).grid(row=5, column=0, sticky='w', pady=5)
        self.preview_label = ttk.Label(main_frame, text="", relief="sunken", width=70, padding=5)
        self.preview_label.grid(row=6, column=0, columnspan=2, sticky='w')
        
        # Pulsante per tradurre il file (stesso stile dei restanti tasti)
        ttk.Button(main_frame, text="TRANSLATE FILE", command=self.start_translation).grid(row=7, column=0, columnspan=2, pady=20)
        
        # Riquadro per i pulsanti di donazione e GitHub
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky='ew')
        ttk.Button(bottom_frame, text="Buy me a coffee", command=self.open_paypal).pack(side='left', padx=5)
        ttk.Button(bottom_frame, text="GitHub", command=self.open_github).pack(side='left', padx=5)
        
        # Barra di stato
        self.status_bar = ttk.Label(self.root, text="Ready", relief='sunken', padding=5)
        self.status_bar.pack(side='bottom', fill='x')
        
    def setup_bindings(self):
        self.output_name_var.trace_add('write', self.update_preview)
        
    def browse_input(self):
        filetypes = [("All text files", "*.*")]
        file = filedialog.askopenfilename(title="Select file to translate", filetypes=filetypes)
        if file:
            self.input_path = file
            self.input_file_var.set(os.path.basename(file))
            self.output_dir = os.path.dirname(file)
            self.input_extension = os.path.splitext(file)[1]
            base_name = os.path.splitext(os.path.basename(file))[0]
            self.output_name_var.set(f"{base_name}_translated")
            self.update_preview()
            
    def browse_output_dir(self):
        initial_dir = self.output_dir if self.output_dir else os.path.expanduser("~")
        dir_selected = filedialog.askdirectory(title="Select destination folder", initialdir=initial_dir)
        if dir_selected:
            self.output_dir = dir_selected
            self.update_preview()
            
    def copy_output_dir(self):
        """Copy output directory to clipboard"""
        if self.output_dir:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.output_dir)
            self.root.update()  # Mantiene il contenuto negli appunti anche dopo la chiusura della finestra
            messagebox.showinfo("Info", "Directory path copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No directory selected!")
            
    def update_preview(self, *args):
        if self.output_dir and self.output_name_var.get() and self.input_extension:
            full_path = os.path.join(self.output_dir, f"{self.output_name_var.get()}{self.input_extension}")
            self.preview_label.config(text=full_path)
        else:
            self.preview_label.config(text="")
            
    def validate_languages(self):
        try:
            # Valida la lingua di destinazione
            dest_lang = self.dest_lang_var.get()
            dest_code = [k for k, v in self.languages.items() if v.lower() == dest_lang.lower()]
            if not dest_code:
                messagebox.showerror("Error", f"Invalid target language: {dest_lang}")
                return None
                
            # Valida la lingua sorgente
            src_lang = self.src_lang_var.get()
            if src_lang.lower() == 'auto':
                return ('auto', dest_code[0])
                
            src_code = [k for k, v in self.languages.items() if v.lower() == src_lang.lower()]
            if not src_code:
                messagebox.showerror("Error", f"Invalid source language: {src_lang}")
                return None
                
            return (src_code[0], dest_code[0])
            
        except Exception as e:
            messagebox.showerror("Error", f"Validation error: {str(e)}")
            return None
            
    def start_translation(self):
        try:
            # Validazione preliminare
            if not self.input_path:
                messagebox.showwarning("Warning", "Select a file to translate!")
                return
                
            if not self.output_name_var.get():
                messagebox.showwarning("Warning", "Enter an output file name!")
                return
                
            # Validazione delle lingue
            lang_codes = self.validate_languages()
            if not lang_codes:
                return
                
            src_code, dest_code = lang_codes
            output_path = self.preview_label.cget("text")
            
            # Lettura del contenuto del file
            try:
                with open(self.input_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
            except Exception as e:
                messagebox.showerror("Read Error", f"Could not read file:\n{str(e)}")
                return
                
            # Traduzione
            self.status_bar.config(text="Translating...")
            self.root.update()
            translated = self.translator.translate(content, src=src_code, dest=dest_code)
            
            # Salvataggio del file tradotto
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(translated.text)
            except Exception as e:
                messagebox.showerror("Save Error", f"Could not save file:\n{str(e)}")
                return
                
            messagebox.showinfo("Success", f"File successfully saved to:\n{output_path}")
            self.status_bar.config(text="Ready")
            
        except Exception as e:
            messagebox.showerror("Error", f"Translation error:\n{str(e)}")
            self.status_bar.config(text="Error")
    
    def open_paypal(self):
        paypal_url = "https://www.paypal.com/paypalme/GabrielPolverini"
        webbrowser.open(paypal_url)
        
    def open_github(self):
        github_url = "https://github.com/Lotverp/Universal-File-Translator"
        webbrowser.open(github_url)

if __name__ == '__main__':
    root = tk.Tk()
    app = UniversalTranslatorApp(root)
    root.mainloop()
