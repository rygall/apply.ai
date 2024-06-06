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

# Provided applicant information
applicant_name = 'Ryan Gallagher'
applicant_town_and_state = 'Media, PA'
applicant_phone_number = '(610) 731-3822'
applicant_personal_email_address = 'ryan.gallagher900@gmail.com'
applicant_work_email_address = 'gallagherj1@leidos.com'

# Experience information
experience = [
    {
        'role': 'Mechanical Engineer',
        'company': 'Leidos',
        'period': 'Current',
        'place': 'Philadelphia, PA',
        'keypoints': [
            'Developed and optimized autonomous auxiliary systems and engine systems for U.S. Navy vessels.',
            'Created software tools, including a feed-forward neural network to predict eductor suction flow rates.',
            'Developed an intuitive GUI application for various computational tasks.',
            'Working on reinforcement learning models to optimize equipment arrangement on naval ships.'
        ]
    }
]

# Education information
education = [
    {
        'title': 'Master of Science in Computer Science',
        'university': 'Expected in Spring 2025',
        'grad_date': 'Spring 2025'
    },
    {
        'title': 'Bachelor of Science in Mechanical Engineering',
        'university': 'Name of University',
        'grad_date': 'Graduation Date: YYYY'
    }
]

# Skills information
skills = [
    {
        'area': 'Machine Learning & AI',
        'description': 'Extensive hands-on experience with PyTorch, NumPy, and Scikit-Learn. Developed neural networks for predictive modeling and optimal system arrangement.'
    },
    {
        'area': 'Software Development',
        'description': 'Proficiency in Python, with practical experience in implementing machine learning algorithms and developing software tools for engineering applications.'
    },
    {
        'area': 'R&D and Customer Engagement',
        'description': 'Proven track record in delivering advanced engineering solutions to both internal and external customers, including the Naval Surface Warfare Center.'
    },
    {
        'area': 'Cross-disciplinary Expertise',
        'description': 'Unique combination of mechanical engineering and computer science, allowing for an integrated approach to developing ML-based engineering solutions.'
    },
    {
        'area': 'Performance Optimization',
        'description': 'Designed and analyzed digital models leading to performance improvements and operational efficiency in complex systems.'
    }
]

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

# Add a section for experience
experience_heading = doc.add_heading('Experience', level=1)
set_paragraph_spacing(experience_heading, space_before=240, space_after=120)

for exp in experience:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=0, space_after=60)
    p.add_run(f"{exp['role']} - {exp['company']}").bold = True
    p.add_run(f"\n{exp['period']} | {exp['place']}")
    for keypoint in exp['keypoints']:
        keypoint_paragraph = doc.add_paragraph(f"• {keypoint}", style='List Bullet')
        set_paragraph_spacing(keypoint_paragraph, space_before=0, space_after=0)

# Add a section for education
education_heading = doc.add_heading('Education', level=1)
set_paragraph_spacing(education_heading, space_before=240, space_after=120)

for edu in education:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=0, space_after=60)
    p.add_run(edu['title']).bold = True
    p.add_run(f"\n{edu['university']}")
    p.add_run(f"\nGraduation Date: {edu['grad_date']}")

# Add a section for skills
skills_heading = doc.add_heading('Skills', level=1)
set_paragraph_spacing(skills_heading, space_before=240, space_after=120)

skills_paragraph = doc.add_paragraph()
set_paragraph_spacing(skills_paragraph, space_before=0, space_after=60)
skills_run = skills_paragraph.add_run()
for skill in skills:
    skills_run.add_text(f"{skill['area']}: {skill['description']}\n")

# Save the document
output_path = 'Ryan_Gallagher_Resume.docx'
doc.save(output_path)
print(f"Document saved as {output_path}")