import tkinter as tk
from tkinter import filedialog
import utilities
import chat

class DocQA_GUI:
    def __init__(self, root):
        self.last_dir = None
        self.file_path = tk.StringVar()
        self.cleaned_text = None

        # Top Section: Document Selection and Actions
        top_frame = tk.Frame(root)
        top_frame.pack(pady=5)

        tk.Button(top_frame, text="Choose Document", command=self.choose_document, width=16).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Send Prompt to LLM", command=self.send_prompt_to_llm, width=16).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Clear", command=self.clear_prompt, width=16).pack(side=tk.LEFT, padx=5) # Added command

        # Displaying the full path and file name
        file_path_frame = tk.Frame(root)
        file_path_frame.pack(pady=1)
        tk.Label(file_path_frame, textvariable=self.file_path).pack(side=tk.LEFT, padx=1)

        # Middle Section: Text Input and Control
        middle_frame = tk.Frame(root)
        middle_frame.pack(pady=5)

        self.text_input = tk.Text(middle_frame, wrap=tk.WORD, height=5)
        self.text_input.pack(side=tk.LEFT, fill=tk.BOTH)
        self.text_input.insert(tk.END, 'Enter prompt here...')
        self.text_input.bind("<FocusIn>", self.clear_placeholder)
        self.text_input.bind("<FocusOut>", self.add_placeholder)

        scroll1 = tk.Scrollbar(middle_frame, command=self.text_input.yview)
        scroll1.pack(side=tk.LEFT, fill=tk.Y)
        self.text_input.config(yscrollcommand=scroll1.set)

        # Bottom Section: Text Output and Actions
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=5)

        self.read_only_text = tk.Text(bottom_frame, wrap=tk.WORD, state=tk.DISABLED, height=20)
        self.read_only_text.pack(side=tk.LEFT, fill=tk.BOTH)

        scroll2 = tk.Scrollbar(bottom_frame, command=self.read_only_text.yview)
        scroll2.pack(side=tk.LEFT, fill=tk.Y)
        self.read_only_text.config(yscrollcommand=scroll2.set)

    def choose_document(self):
        file_types = [("Documents", "*.pdf *.docx *.txt *.doc *.py *.rtf"), ("All Files", "*.*")]
        file_path = filedialog.askopenfilename(initialdir=self.last_dir, filetypes=file_types)
        if file_path:
            self.last_dir = file_path.rsplit('/', 1)[0]
            self.file_path.set(file_path)
            self.cleaned_text = utilities.process_file(file_path)

    def clear_prompt(self):
        self.text_input.delete("1.0", tk.END)

    def clear_placeholder(self, event=None):
        if self.text_input.get("1.0", tk.END).strip() == 'Enter prompt here...':
            self.text_input.delete("1.0", tk.END)

    def add_placeholder(self, event=None):
        if not self.text_input.get("1.0", tk.END).strip():
            self.text_input.insert(tk.END, 'Enter prompt here...')

    def send_prompt_to_llm(self):
        if self.cleaned_text:
            user_prompt = self.text_input.get("1.0", tk.END).strip()
            
            full_text = user_prompt + " " + self.cleaned_text
            
            response = chat.get_completion(full_text)

            self.read_only_text.config(state=tk.NORMAL)
            self.read_only_text.delete("1.0", tk.END)
            self.read_only_text.insert(tk.END, response)
            self.read_only_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DocQA GUI")
    root.geometry("800x600")
    app = DocQA_GUI(root)
    root.mainloop()
