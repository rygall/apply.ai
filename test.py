from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Function to set paragraph spacing
def set_paragraph_spacing(paragraph, space_before=0, space_after=0, line_spacing=1):
    p_pr = paragraph._element.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(space_before))
    spacing.set(qn('w:after'), str(space_after))
    spacing.set(qn('w:line'), str(line_spacing * 240))  # 240 is the default line height unit
    p_pr.append(spacing)

applicant_name = 'Ryan Gallagher'
applicant_town_and_state = 'Media, PA'
applicant_phone_number = '(610) 731-3822'
applicant_personal_email_address = 'ryan.gallagher900@gmail.com'
applicant_work_email_address = 'gallagherj1@leidos.com'

# Create a new Document
doc = Document()

# Add a title
title = doc.add_heading(applicant_name, 0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_paragraph_spacing(title, space_before=0, space_after=240)  # Add some space after the title

# Add a section for contact info
contact_info = doc.add_paragraph()
contact_info.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_paragraph_spacing(contact_info, space_before=0, space_after=240)  # Add some space after contact info
contact_info.add_run(applicant_town_and_state + ' | ').bold = True
contact_info.add_run(applicant_phone_number + ' | ')
contact_info.add_run(applicant_personal_email_address + ' | ')
contact_info.add_run(applicant_work_email_address)

# Add a section for summary
summary_heading = doc.add_heading('SUMMARY', level=1)
set_paragraph_spacing(summary_heading, space_before=240, space_after=120)

summary = (
    "Dynamic and results-driven Mechanical Engineer with extensive experience in machine learning and AI development, "
    "currently pursuing a Master’s degree in Computer Science with a focus on artificial intelligence and machine learning. "
    "Proven ability to design and deploy autonomous systems and machine learning models to optimize performance and efficiency. "
    "Skilled in MLOps practices, advanced Python programming, and cloud infrastructure management. "
    "Seeking a role as a Senior Machine Learning Engineer to leverage technical expertise and innovation in a challenging environment."
)

summary_paragraph = doc.add_paragraph(summary)
set_paragraph_spacing(summary_paragraph, space_before=0, space_after=240)

# Add a section for skills
skills_heading = doc.add_heading('SKILLS', level=1)
set_paragraph_spacing(skills_heading, space_before=240, space_after=120)

skills = [
    "Languages: C, Java, Python",
    "Libraries & Tools: NumPy, PyTorch, Pandas, Scikit-Learn, TensorFlow, Kubeflow, MLflow, TensorBoard, Jupyter Notebooks",
    "Version Control: Git, GitHub",
    "MLOps & DevOps: Docker, CI/CD frameworks, Kubernetes, Infrastructure-as-Code (Terraform, Ansible)",
    "Modeling & Simulation: PIPE-FLO, MATLAB",
    "Computer-Aided Design: AutoCAD, SolidWorks",
    "Other Tools: AI Explainability and Monitoring tools, CloudFormation, GitLab, Nexus"
]

skills_paragraph = doc.add_paragraph()
set_paragraph_spacing(skills_paragraph, space_before=0, space_after=60)
skills_run = skills_paragraph.add_run()
for skill in skills:
    skills_run.add_text(f"{skill}\n")

# Add a section for experience
experience_heading = doc.add_heading('EXPERIENCE', level=1)
set_paragraph_spacing(experience_heading, space_before=240, space_after=120)

experience = [
    {
        'role': 'Mechanical Engineer',
        'company': 'Leidos, Philadelphia, PA',
        'period': 'May 2020 - Present',
        'keypoints': [
            "Designed and implemented autonomous systems for U.S. Navy and DARPA unmanned surface vessels.",
            "Developed digital models and optimized performance of auxiliary systems using simulation.",
            "Analyzed data to optimize engine systems and reduce operating times.",
            "Provided engineering support for the Naval Surface Warfare Center’s DDG(X) program.",
            "Developed machine learning models and software tools:",
            " - Trained neural networks for predicting system performance in partially-observable environments.",
            " - Developed GUI-based programs for engineering computations.",
            " - Created reinforcement learning models for equipment arrangement on ships."
        ]
    },
    {
        'role': 'Mechanical Engineering Intern',
        'company': 'Monroe Energy, LLC, Trainer, PA',
        'period': 'May - August, 2016 - 2019',
        'keypoints': []
    }
]

for exp in experience:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=0, space_after=60)
    p.add_run(f"{exp['role']} - {exp['company']}").bold = True
    p.add_run(f"\n{exp['period']}")
    for keypoint in exp['keypoints']:
        keypoint_paragraph = doc.add_paragraph(f"• {keypoint}", style='List Bullet')
        set_paragraph_spacing(keypoint_paragraph, space_before=0, space_after=0)

# Add a section for education
education_heading = doc.add_heading('EDUCATION', level=1)
set_paragraph_spacing(education_heading, space_before=240, space_after=120)

education = [
    {
        'title': 'Master of Science, Computer Science (AI/ML focus)',
        'university': 'Drexel University, Philadelphia, PA',
        'grad_date': '2021 - Present',
        'gpa': '3.93',
        'minor': None
    },
    {
        'title': 'Bachelor of Science, Mechanical Engineering',
        'university': 'Thomas Jefferson University, Philadelphia, PA',
        'grad_date': '2018 - 2020',
        'gpa': '3.39',
        'minor': None
    },
    {
        'title': 'Bachelor of Science, Physics',
        'university': 'West Chester University of Pennsylvania, West Chester, PA',
        'grad_date': '2015 - 2018',
        'gpa': '3.11',
        'minor': 'Mathematics'
    }
]

for edu in education:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=0, space_after=60)
    p.add_run(edu['title']).bold = True
    p.add_run(f"\n{edu['university']}")
    p.add_run(f"\nGraduation Date: {edu['grad_date']}")
    if 'gpa' in edu:
        p.add_run(f"\nGPA: {edu['gpa']}")
    if 'minor' in edu:
        p.add_run(f"\nMinor: {edu['minor']}")

# Save the document
output_path = 'Resume.docx'
doc.save(output_path)

print(f"Document saved as {output_path}")