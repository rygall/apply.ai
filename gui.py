import customtkinter as ctk
import warnings
import tkinter as tk
from tkinter import filedialog,PhotoImage
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from selenium import webdriver
import tiktoken
from pdfminer.high_level import extract_text


warnings.filterwarnings("ignore", message=".*CTkImage.*HighDPI displays.*")

ctk.set_appearance_mode("Dark")      # GUI theme
ctk.set_default_color_theme("blue")  # color theme

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('Apply.ai Application')
        self.geometry('600x700')

        original_image = Image.open('logo-no-background.png')
        resized_image = original_image.resize((75, 75))
        self.image = ImageTk.PhotoImage(resized_image)

        # Image Label
        self.image_label = ctk.CTkLabel(self, text = "" , image=self.image)
        self.image_label.pack(pady=30)

        # URL Entry
        self.url_label = ctk.CTkLabel(self, text="Enter Job Listing URL:")
        self.url_label.pack(pady=10)
        self.url_entry = ctk.CTkEntry(self, width=400, placeholder_text="https://job_listing.com")
        self.url_entry.pack(pady=10)

        # PDF Entry and Load Button
        self.pdf_label = ctk.CTkLabel(self, text="Upload Your PDF Resume:")
        self.pdf_label.pack(pady=10)
        self.pdf_entry_frame = ctk.CTkFrame(self)
        self.pdf_entry_frame.pack(pady=10)
        self.pdf_entry = ctk.CTkEntry(self.pdf_entry_frame, width=340, placeholder_text="resume.pdf")
        self.pdf_entry.configure(state='disabled')
        self.pdf_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.load_button = ctk.CTkButton(self.pdf_entry_frame, text="Upload File", command=self.load_pdf)
        self.load_button.pack(side=tk.RIGHT, padx=10)

        # Process Button
        self.process_button = ctk.CTkButton(self, text="Process", command=self.process_input)
        self.process_button.pack(pady=20)


        # Input / Output Separator
        self.separator_frame = ctk.CTkFrame(self, height=2, fg_color=self.process_button.cget('fg_color'))
        self.separator_frame.pack(fill='x', padx=50)

        # Output Text Box
        self.output_label = ctk.CTkLabel(self, text="Skill Recommendations:")
        self.output_label.pack(pady=10)
        self.output_box = ctk.CTkTextbox(self, height=100, width=400, state='disabled')
        self.output_box.pack(pady=10)

        # Output / Test Separator
        self.separator_frame = ctk.CTkFrame(self, height=2, fg_color=self.process_button.cget('fg_color'))
        self.separator_frame.pack(fill='x', padx=50)

        # Testing Output
        self.test_label = ctk.CTkLabel(self, text="Testing Results:")
        self.test_label.pack(pady=10)

        # Scores Frame
        self.scores_frame = ctk.CTkFrame(self)
        self.scores_frame.pack(pady=10)

        # Original Resume Score Text Box
        self.original_score_label = ctk.CTkLabel(self.scores_frame, text="Original Resume Score:")
        self.original_score_label.pack(side=tk.LEFT, padx=10)
        self.original_score_box = ctk.CTkTextbox(self.scores_frame, height=10, width=50, state='disabled')
        self.original_score_box.pack(side=tk.LEFT, padx=10)

        # Improved Resume Score Text Box
        self.improved_score_label = ctk.CTkLabel(self.scores_frame, text="Apply.ai Resume Score:")
        self.improved_score_label.pack(side=tk.LEFT, padx=10)
        self.improved_score_box = ctk.CTkTextbox(self.scores_frame, height=10, width=50, state='disabled')
        self.improved_score_box.pack(side=tk.LEFT, padx=10)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_entry.configure(state='normal')
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, file_path)
            self.pdf_entry.configure(state='disabled')

    def process_input(self):
        url = self.url_entry.get()
        pdf_path = self.pdf_entry.get()

        # Convert URL Job Listing to Text
        self.listing = self.extract_listing(url)

        # Convert PDF Resume Text
        self.input_pdf = self.pdf_to_text(pdf_path)

        output_text = f"Processed URL: {url} \n PDF: {pdf_path}"
        self.output_box.configure(state='normal')
        self.output_box.delete('1.0', tk.END)
        self.output_box.insert(tk.END, output_text)
        self.output_box.configure(state='disabled')
        # Tokenize the prompt
        encoding = tiktoken.get_encoding("o200k_base")
        num_tokens = len(encoding.encode(self.listing))
        # Count the number of tokens
        print("Job listing is " +str(num_tokens)+ " tokens")
        print(self.listing)
        print(self.input_pdf)


    def extract_listing(self, url):
        # initialize a new browser (in this case, we're using Chrome)
        browser = webdriver.Chrome()
        # tell the browser to retrieve the content of the url
        browser.get(str(url))
        # get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        return soup.text

    def pdf_to_text(self, pdf_path):
        # Extract text from the PDF file
        text = extract_text(pdf_path)
        return text

    def test_resume(self):
        print("TEST")

if __name__ == "__main__":
    app = App()
    app.mainloop()
