import customtkinter as ctk
import warnings
import tkinter as tk
from tkinter import filedialog,PhotoImage
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from selenium import webdriver
import tiktoken
from pdfminer.high_level import extract_text

from openai import OpenAI
client = OpenAI()

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
        input_pdf_text = self.pdf_to_text(pdf_path)

        output_text = f"Processed URL: {url} \n PDF: {pdf_path}"
        self.output_box.configure(state='normal')
        self.output_box.delete('1.0', tk.END)
        self.output_box.insert(tk.END, output_text)
        self.output_box.configure(state='disabled')
        # Tokenize the prompt
        encoding = tiktoken.get_encoding("o200k_base")
        num_tokens = len(encoding.encode(self.listing))
        # Count the number of tokens
        print("Job listing is " + str(num_tokens) + " tokens")
        
        parsed_listing = self.extract_relevant_info(self.listing)
        print("======PARSED LISTING======")
        print(parsed_listing)
        print("======END PARSED LISTING======")

        self.generate_resume(parsed_listing, input_pdf_text)
        self.generate_cv(parsed_listing, input_pdf_text)

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

    def extract_relevant_info(self, listing):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert at parsing through data and extracting relevant information."},
                {"role": "user", "content": "You are going to be provided a large string, within that string is information on a job listing. Extract all information for the job listing."},
                {"role": "user", "content": listing}
            ],
            temperature=0.7
        )
        return completion.choices[0].message.content

    def generate_resume(self, listing, resume):
        resume_text = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're an experienced writer who specializes in assisting people with job applications."},
                {"role": "user", "content": "I am going to provide you with my resume and a job listing, please provide me with a resume that is tweaked for the job listing. Don't make anything up about me."},
                {"role": "user", "content": resume},
                {"role": "user", "content": listing},
            ],
            temperature=1
        )

        template_res = None
        with open("template_res.py", 'r') as file:
            template_res = file.read()

        resume_code = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant with a focus on processing and integrating textual information."},
                {"role": "user", "content": "You will be provided with Python code that generates a template for a resume. You will also be provided text for a cover letter. Fill in the template using the provided text for the cover letter. Keep changes to the format of the document to a minimum."},
                {"role": "user", "content": template_res},
                {"role": "user", "content": resume_text.choices[0].message.content},
            ],
            temperature=0.5
        )
        print(resume_code.choices[0].message.content)
    

    def generate_cv(self, listing, resume):
        cv_text = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're an experienced writer who specializes in assisting people with job applications."},
                {"role": "user", "content": "I am going to provide you with my resume and a job listing, please provide me with a cover that is tailored for the job listing. Don't make anything up about me."},
                {"role": "user", "content": resume},
                {"role": "user", "content": listing},
            ],
            temperature=1
        )

        template_cv = None
        with open("template_cv.py", 'r') as file:
            template_cv = file.read()

        cv_code = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant with a focus on processing and integrating textual information."},
                {"role": "user", "content": "You will be provided with Python code that generates a template for a cover letter. You will also be provided text for a cover letter. Fill in the template using the provided text for the cover letter. Keep changes to the format of the document to a minimum."},
                {"role": "user", "content": template_cv},
                {"role": "user", "content": cv_text.choices[0].message.content},
            ],
            temperature=0.5
        )
        print(cv_code.choices[0].message.content)


        
if __name__ == "__main__":
    app = App()
    app.mainloop()
