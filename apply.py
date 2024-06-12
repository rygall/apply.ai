import customtkinter as ctk
import warnings
import tkinter as tk
from tkinter import filedialog,PhotoImage
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from selenium import webdriver
import tiktoken
from pdfminer.high_level import extract_text
import threading
from openai import OpenAI
client = OpenAI()

warnings.filterwarnings("ignore", message=".*CTkImage.*HighDPI displays.*")

ctk.set_appearance_mode("Dark")      # GUI theme
ctk.set_default_color_theme("blue")  # color theme

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title('Apply.ai Application')
        self.geometry('700x800')

        original_image = Image.open('utils\\logo-no-background.png')
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

        # Progress LED Indicators
        background_color = "#2b2b2b"  # This is an example, replace with the actual color
        self.led_frame = ctk.CTkFrame(self)
        self.led_frame.pack(pady=10)
        self.leds = []
        self.led_labels = ["Extract Listing", "Extract Resume", "Generate Resume", "Generate Cover Letter",
                           "Evaluate"]
        for i in range(5):
            led_label = ctk.CTkLabel(self.led_frame, text=self.led_labels[i])
            led_label.pack(side=tk.LEFT, padx=5)

            # Create a canvas for the LED with the same background color as your GUI
            led_canvas = tk.Canvas(self.led_frame, width=20, height=20, bg=background_color, highlightthickness=0)
            led_canvas.pack(side=tk.LEFT, padx=5)

            # Draw a circle on the canvas to represent the LED
            led = led_canvas.create_oval(5, 5, 15, 15, fill="red", outline="black")
            self.leds.append(led)

        # Input / Output Separator
        self.separator_frame = ctk.CTkFrame(self, height=2, fg_color=self.process_button.cget('fg_color'))
        self.separator_frame.pack(fill='x', padx=50)

        # Output Text Box
        self.output_label = ctk.CTkLabel(self, text="Skill Recommendations")
        self.output_label.pack(pady=10)
        self.output_box = ctk.CTkTextbox(self, height=100, width=400, state='disabled')
        self.output_box.pack(pady=10)

        # Qualifications Met Percentage
        self.qual_percentage_label = ctk.CTkLabel(self, text="Qualifications Met")
        self.qual_percentage_label.pack(padx=10)
        self.qual_percentage_box = ctk.CTkTextbox(self, height=10, width=100, state='disabled')
        self.qual_percentage_box.pack(padx=10, pady=10)

        # Output / Test Separator
        self.separator_frame = ctk.CTkFrame(self, height=2, fg_color=self.process_button.cget('fg_color'))
        self.separator_frame.pack(fill='x', padx=70)

        # Testing Output
        self.test_label = ctk.CTkLabel(self, text="Testing Results:")
        self.test_label.pack(pady=10)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_entry.configure(state='normal')
            self.pdf_entry.delete(0, tk.END)
            self.pdf_entry.insert(0, file_path)
            self.pdf_entry.configure(state='disabled')

    def process_input(self):
        self.change_led_color(0, "red")
        self.change_led_color(1, "red")
        self.change_led_color(2, "red")
        self.change_led_color(3, "red")
        self.change_led_color(4, "red")

        # Create a new thread for the long-running tasks
        threading.Thread(target=self.main_tasks).start()

    def main_tasks(self):
        # extract job listing and convert to concise text
        parsed_listing = self.extract_job_listing()

        # extract text from resume pdf
        self.change_led_color(1, "yellow")
        pdf_path = self.pdf_entry.get()
        input_pdf_text = self.pdf_to_text(pdf_path)
        self.change_led_color(1, "green")

        # generate resume
        self.change_led_color(2, "yellow")
        resume_text = self.generate_resume(parsed_listing, input_pdf_text)
        resume_code = self.extract_substring(resume_text)
        print(parsed_listing)
        print(resume_text)
        print(resume_code)
        max_retries = 5  # Set a limit to avoid infinite loops
        attempts = 0
        while attempts < max_retries:
            try:
                exec(resume_code, globals())
                print("Code executed successfully.")
                break
            except Exception as e:
                attempts += 1
                print(f"Attempt {attempts} failed with error: {e}")
        if attempts == max_retries:
            print("Reached the maximum number of retries. Code execution failed.")
        self.change_led_color(2, "green")

        # generate cover letter
        self.change_led_color(3, "yellow")
        cv_text = self.generate_cv(parsed_listing, input_pdf_text)
        cv_code = self.extract_substring(cv_text)
        attempts = 0
        while attempts < max_retries:
            try:
                exec(cv_code, globals())
                print("CV code executed successfully.")
                break
            except Exception as e:
                attempts += 1
                print(f"CV code attempt {attempts} failed with error: {e}")

        if attempts == max_retries:
            print("Reached the maximum number of retries for CV code. Execution failed.")
        exec(cv_code, globals())
        self.change_led_color(3, "green")

        # evaluate
        self.change_led_color(4, "yellow")
        self.evaluation(parsed_listing, resume_text, cv_text)
        self.change_led_color(4, "green")

    def extract_job_listing(self):
        # extract the job listing text from the website
        self.change_led_color(0, "yellow")
        max_attempts = 5
        attempt = 0
        listing = None
        success = False
        url = self.url_entry.get()
        while not success and attempt < max_attempts:
            listing, num_tokens = self.extract_and_count_tokens(url)
            attempt += 1
            if num_tokens > 10:
                success = True
        if success:
            # Code to run after a successful extraction
            print("Successfully extracted the listing with more than 10 tokens.")
        else:
            # Code to run after reaching the maximum number of attempts
            print("Failed to extract a listing with more than 10 tokens after max attempts.")

        # extract the relevant text for the job listing
        parsed_listing = self.extract_relevant_info(listing)
        self.change_led_color(0, "green")
        return parsed_listing
    
    def extract_and_count_tokens(self, url):
        # Convert URL job Listing to Text
        listing = self.extract_listing(url)
        
        # Tokenize the job listing text
        encoding = tiktoken.get_encoding("o200k_base")
        num_tokens = len(encoding.encode(listing))
        
        return listing, num_tokens
    
    def pdf_to_text(self, pdf_path):
        # Extract text from the PDF file
        text = extract_text(pdf_path)
        return text

    def extract_listing(self, url):
        # initialize a new browser (in this case, we're using Chrome)
        browser = webdriver.Chrome()
        # tell the browser to retrieve the content of the url
        browser.get(str(url))
        # get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        return soup.text

    def extract_relevant_info(self, listing):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are going to be provided a large string, within that string is information on a job listing. Extract all information for the job listing."},
                {"role": "user", "content": listing}
            ]
        )
        return completion.choices[0].message.content

    def generate_resume(self, listing, resume):
        resume_text = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are going to be provided with a resume and a job listing, please write a resume that is tailored for the job listing. Don't make anything up about the applicant."},
                {"role": "user", "content": resume},
                {"role": "user", "content": listing},
            ]
        )

        template_res = None
        with open("utils\\template_res.py", 'r') as file:
            template_res = file.read()

        resume_code = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will be provided with Python code that generates a template for a resume. You will also be provided text that is for a resume. Fill in the template using the provided text for the resume. Keep changes to the format of the word document to a minimum. Don't make information up about the applicant."},
                {"role": "user", "content": template_res},
                {"role": "user", "content": resume_text.choices[0].message.content},
            ]
        )
        return resume_code.choices[0].message.content

    def generate_cv(self, listing, resume):
        cv_text = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are going to be provided with a resume and a job listing, please write a cover that is tailored for the job listing. Don't make anything up about the applicant."},
                {"role": "user", "content": resume},
                {"role": "user", "content": listing},
            ]
        )

        template_cv = None
        with open("utils\\template_cv.py", 'r') as file:
            template_cv = file.read()

        cv_code = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will be provided with Python code that generates a template for a cover letter. You will also be provided text that is for a cover letter. Fill in the template using the provided text for the cover letter. Keep changes to the format of the word document to a minimum. Don't make information up about the applicant."},
                {"role": "user", "content": template_cv},
                {"role": "user", "content": cv_text.choices[0].message.content},
            ]
        )
        return cv_code.choices[0].message.content

    def extract_substring(self, text):
        try:
            start_index = text.index("```python") + len("```python")
            end_index = text.index("```", start_index)
            return text[start_index:end_index]
        except ValueError:
            return text
        
    def evaluation(self, job_listing, resume, cv):
        # gather qualifications list
        qualificaiton_string = self.generate_qualifications_string(job_listing)
        qualification_list = self.parse_qualifications_string(qualificaiton_string)

        # generate applicant match score
        res_score, results_list = self.evaluate_resume(qualification_list, resume)

        self.output_box.configure(state='normal')
        self.output_box.delete('1.0', tk.END)
        for i in range(len(results_list)):
            if results_list[i] == 0:
                output_text = qualification_list[i] + "\n"
                self.output_box.insert(tk.END, output_text)
        self.output_box.configure(state='disabled')

        self.qual_percentage_box.configure(state='normal')  # Change state to 'normal'
        self.qual_percentage_box.delete(1.0, 'end')  # Clear the box
        self.qual_percentage_box.insert('end', str(round(res_score))+"%")  # Insert new data
        self.qual_percentage_box.configure(state='disabled')

        print("Generated Applicant Match Score:", res_score, "%")

    def generate_qualifications_string(self, listing):
        qual_list = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will be provided with a job listing. Please extract the jobs qualifications, then format them into a list. Your response should be one single string, where each requirement or qualification is separated by a semicolon."},
                {"role": "user", "content": listing},
            ]
        )
        return qual_list.choices[0].message.content

    def parse_qualifications_string(self, input_string):
        return input_string.split(';')

    def evaluate_resume(self, qualification_list, resume):
        results = []
        for qualification in qualification_list:
            print("Qualification:", qualification)
            satisifed = self.determine_satisfied(qualification, resume)
            print("Satisfied:", satisifed)
            results.append(int(satisifed))
        print("Results List:", results)
        resume_score = self.satisfied_percentage(results)
        return resume_score, results
    
    def determine_satisfied(self, qualification, resume):
        qual_list = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will be provided with a specific qualificaiton for a job listing and also a resume that will be submitted in an application to that job listing. Please respond the number 1 if the qualification is satisfied, or the number 0 if it is not satisfied. Don't respond with anything but 1 or 0."},
                {"role": "user", "content": qualification},
                {"role": "user", "content": resume}
            ],
            temperature=0.3
        )
        return qual_list.choices[0].message.content

    def satisfied_percentage(self, number_list):
        # Count the number of 1's in the list
        count_of_ones = number_list.count(1)
        # Calculate the percentage of 1's
        percentage_of_ones = (count_of_ones / len(number_list)) * 100 if number_list else 0
        return percentage_of_ones

    def change_led_color(self, led_index, new_color):
        # Get the canvas that contains the LED
        led_canvas = self.led_frame.winfo_children()[led_index * 2 + 1]

        # Change the color of the LED
        led_canvas.itemconfig(self.leds[led_index], fill=new_color)


if __name__ == "__main__":
    app = App()
    app.mainloop()
