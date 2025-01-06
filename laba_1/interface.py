import tkinter as tk
from tkinter import scrolledtext
from api1 import Api1
from api2 import Api2

class Application(tk.Tk):
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.ai_gpt_detector = Api1(api_key)
        self.ai_6_detector = Api2(api_key)
        self.text_input = tk.Text(self, height=10, width=50)
        self.text_input.pack()
        self.ai_gpt_output = scrolledtext.ScrolledText(self, height=10, width=50)
        self.ai_gpt_output.pack()
        self.ai_6_output = scrolledtext.ScrolledText(self, height=10, width=50)
        self.ai_6_output.pack()
        
        self.ai_gpt_button = tk.Button(self, text='Detect with AI-GPT', command=self.detect_ai_gpt)
        self.ai_gpt_button.pack()
        self.ai_6_button = tk.Button(self, text='Detect with AI-6', command=self.detect_ai_6)
        self.ai_6_button.pack()

        self.paste_button = tk.Button(self, text='Paste from Clipboard', command=self.paste_from_clipboard)
        self.paste_button.pack()

    def detect_ai_gpt(self):
        text = self.text_input.get('1.0', tk.END)
        result = str(self.ai_gpt_detector.detect(text)['fakePercentage'])
        self.ai_gpt_output.delete('1.0', tk.END)
        self.ai_gpt_output.insert('1.0', f'The probability of AI generation according to the first model : {result}')

    def detect_ai_6(self):
        text = self.text_input.get('1.0', tk.END)
        result = str(self.ai_6_detector.detect(text)['probabilities']['ai'])
        self.ai_6_output.delete('1.0', tk.END)
        self.ai_6_output.insert('1.0', f'The probability of AI generation according to the second model : {result}')

    def paste_from_clipboard(self):
        try:
            clipboard_text = self.clipboard_get()  # Получить текст из буфера обмена
            self.text_input.delete('1.0', tk.END)  # Очистить текущее содержимое
            self.text_input.insert('1.0', clipboard_text)  # Вставить текст в поле ввода
        except tk.TclError:
            self.text_input.insert('1.0', "No text in clipboard")

if __name__ == '__main__':
    API_KEY = '2bd11f7ddemsh4108148ab3de41cp1e6509jsnd4b6c49635f1'
    app = Application(API_KEY)
    app.mainloop()
