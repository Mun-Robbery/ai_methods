import tkinter as tk
from tkinter import ttk
from gpt_api import GptApi

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATI ruGPT-3 Query Interface")
        self.geometry("800x600")

        # Поле ввода запроса
        self.query_label = tk.Label(self, text="Enter your query:")
        self.query_label.pack()
        self.query_entry = tk.Text(self, height=5, width=50)
        self.query_entry.pack()

        # Кнопка для вставки из буфера обмена
        self.paste_button = tk.Button(self, text="Paste from Clipboard", command=self.paste_from_clipboard)
        self.paste_button.pack()

        # Поля для ввода параметров генерации
        self.param_frame = tk.Frame(self)
        self.param_frame.pack()
        self.param_labels = ["max_length", "repetition_penalty", "top_k", "top_p", "temperature", "no_repeat_ngram_size"]
        self.param_entries = []
        for i, label in enumerate(self.param_labels):
            param_label = tk.Label(self.param_frame, text=label)
            param_label.grid(row=i, column=0)
            param_entry = tk.Entry(self.param_frame, width=20)
            param_entry.grid(row=i, column=1)
            self.param_entries.append(param_entry)

        # Списки для выбора параметров генерации
        self.dropdown_frame = tk.Frame(self)
        self.dropdown_frame.pack()
        self.dropdown_labels = ["do_sample", "num_beams"]
        self.dropdown_options = [
            ["True", "False"],
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        ]
        self.dropdown_variables = []
        for i, label in enumerate(self.dropdown_labels):
            dropdown_label = tk.Label(self.dropdown_frame, text=label)
            dropdown_label.grid(row=i, column=0)
            dropdown_variable = tk.StringVar()
            dropdown_variable.set(self.dropdown_options[i][0])
            dropdown_menu = ttk.OptionMenu(self.dropdown_frame, dropdown_variable, *self.dropdown_options[i])
            dropdown_menu.grid(row=i, column=1)
            self.dropdown_variables.append(dropdown_variable)

        # Окно вывода
        self.output_label = tk.Label(self, text="Model Output:")
        self.output_label.pack()
        self.output_window = tk.Text(self, height=10, width=50)
        self.output_window.pack()

        # Кнопка для копирования текста из поля вывода
        self.copy_button = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack()

        # Кнопка вывода генерации 
        self.generate_button = tk.Button(self, text="Generate Output", command=self.generate_output)
        self.generate_button.pack()

    def paste_from_clipboard(self):
        """Вставляет текст из буфера обмена в поле ввода запроса."""
        try:
            clipboard_text = self.clipboard_get()
            self.query_entry.insert(tk.END, clipboard_text)
        except tk.TclError:
            self.query_entry.insert(tk.END, "Clipboard is empty or unavailable.")

    def copy_to_clipboard(self):
        """Копирует текст из поля вывода в буфер обмена."""
        output_text = self.output_window.get("1.0", tk.END).strip()
        if output_text:
            self.clipboard_clear()
            self.clipboard_append(output_text)
            self.update()  # Обновить буфер обмена

    def generate_output(self):
        # Сбор информации для генерации
        query = self.query_entry.get("1.0", tk.END)
        param_values = [entry.get() for entry in self.param_entries]
        dropdown_values = [variable.get() for variable in self.dropdown_variables]

        # Генерация 
        gpt_api = GptApi(query=query) 
        output = gpt_api.get_answer(dict(zip(self.param_labels, param_values)) | dict(zip(self.dropdown_labels, dropdown_values)))

        # Отображение вывода
        self.output_window.delete("1.0", tk.END)
        self.output_window.insert("1.0", output)

if __name__ == "__main__":
    app = Application()
    app.mainloop()