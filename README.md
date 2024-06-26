# Installation
## Clone the Repository

    git clone https://github.com/rygall/apply.ai.git

## Install Required Packages

    cd apply.ai
    pip install -r requirements.txt

## Enter the OPENAI Key
    We provided an OPENAI key in the submission comments. Please place that key into Line 14 of apply.py.

# Running the Program
To run the program, enter the following command:

    python apply.py 
    
When the GUI appears, first copy and paste a URL to a job listing in the "Enter Job Listing URL" text box.

Next upload a pdf of a resume using the "Upload File" button to choose a file from your file system. (In the "test_resumes" folder)

Lastly, click the "Process" button. The program will run in the background.

Progress can be kept track of using the LED indicators. When all are green, the process and testing has completed

Results are saved in the _**results**_ folder.

# Examples
There are examples of generated resumes and cover letters in the _**result**_ folder.

The Robert Borrelli cover letter and resume were generated based on the following job listing:

    https://careers.leidos.com/jobs/14098966-software-engineer

The Ryan Gallagher cover letter and resume were generated based on the following job listing:

    https://boards.greenhouse.io/andurilindustries/jobs/4196647007?gh_jid=4196647007

The Lauren Chen cover letter and resume were generated based on the following job listing:

    https://careers.leidos.com/jobs/14522302-senior-marketing-and-communications-manager


    
