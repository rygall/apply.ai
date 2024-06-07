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


applicant_name = 'RYAN GALLAGHER'
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
summary = doc.add_paragraph()
summary.add_run(
    "Experienced Mechanical Engineer with a focus on design, modeling, and optimization for military and industrial applications. "
    "Proficient in AutoCAD and possess a strong background in project management, construction inspections, and coordination with multidisciplinary teams. "
    "Seeking to leverage expertise in a Civil Engineering role to contribute to high-impact projects at Leidos."
)

# Add a section for skills
skills_heading = doc.add_heading('SKILLS', level=1)
set_paragraph_spacing(skills_heading, space_before=240, space_after=120)
skills = doc.add_paragraph()
skills.add_run(
    "- Engineering Design & Software: AutoCAD, SolidWorks, PIPE-FLO\n"
    "- Programming Languages: C, Java, Python\n"
    "- Data Analysis Libraries: NumPy, PyTorch, Pandas, Scikit-Learn\n"
    "- Version Control Systems: Git, GitHub\n"
    "- Simulation Tools: MATLAB"
)

# Add a section for experience
experience_heading = doc.add_heading('EXPERIENCE', level=1)
set_paragraph_spacing(experience_heading, space_before=240, space_after=120)

experience = [
    {
        'role': 'Mechanical Engineer',
        'company': 'Leidos, Philadelphia, PA',
        'period': 'May 2020 - Present',
        'place': '',
        'keypoints': [
            'Designed fully autonomous auxiliary systems for U.S. Navy and DARPA unmanned surface vessels.',
            'Developed digital models of auxiliary systems to optimize performance.',
            'Provided engineering support for the Naval Surface Warfare Center\'s DDG(X) land-based test site.',
            'Analyzed data to support modification proposals for LPD 17 class ships, improving operational efficiency.',
            'Developed software including feed-forward neural networks and reinforcement learning models to enhance ship design processes.'
        ]
    },
    {
        'role': 'Mechanical Engineering Intern',
        'company': 'Monroe Energy, LLC, Trainer, PA',
        'period': 'May 2016 - August 2019',
        'place': '',
        'keypoints': [
            'Assisted with on-site surveys and developed detailed engineering reports.',
            'Participated in construction inspections and coordinated with team members to resolve design issues.',
            'Utilized AutoCAD for the preparation of construction drawings and project specifications.',
            'Supported the preparation of project management documentation, including safety plans and risk assessments.'
        ]
    }
]

for exp in experience:
    p = doc.add_paragraph()
    set_paragraph_spacing(p, space_before=0, space_after=60)
    p.add_run(f"{exp['role']} - {exp['company']}").bold = True
    p.add_run(f"\n{exp['period']} | {exp['place']}")
    for keypoint in exp['keypoints']:
        keypoint_paragraph = doc.add_paragraph(f"• {keypoint}", style='List Bullet')
        set_paragraph_spacing(keypoint_paragraph, space_before=0, space_after=0)

# Add a section for education
education_heading = doc.add_heading('EDUCATION', level=1)
set_paragraph_spacing(education_heading, space_before=240, space_after=120)

education = [
    {
        'title': 'Master of Science, Computer Science',
        'university': 'Drexel University, Philadelphia, PA',
        'grad_date': '2021-Present',
        'gpa': '3.93',
        'additional_info': 'Focus: Artificial Intelligence and Machine Learning\nExpected Graduation: Spring 2025'
    },
    {
        'title': 'Bachelor of Science, Mechanical Engineering',
        'university': 'Thomas Jefferson University, Philadelphia, PA',
        'grad_date': '2018 - 2020',
        'gpa': '3.39'
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
    if 'additional_info' in edu:
        p.add_run(f"\n{edu['additional_info']}")

# Add a section for certifications and clearances
certifications_heading = doc.add_heading('CERTIFICATIONS AND CLEARANCES', level=1)
set_paragraph_spacing(certifications_heading, space_before=240, space_after=120)
certifications = doc.add_paragraph()
certifications.add_run('[Add any relevant certifications or clearances you have here, if applicable]')

# Add a section for professional strengths
strengths_heading = doc.add_heading('PROFESSIONAL STRENGTHS', level=1)
set_paragraph_spacing(strengths_heading, space_before=240, space_after=120)
strengths = doc.add_paragraph()
strengths.add_run(
    "- Strong understanding of structural design, including foundations and industrial structural systems.\n"
    "- Extensive experience with AutoCAD and other design software for the creation of precise engineering drawings.\n"
    "- Proven ability to manage multiple concurrent projects, ensuring timely and successful completion.\n"
    "- Effective communicator, capable of delivering clear and concise technical documentation and coordinating with diverse stakeholders.\n"
    "- Knowledgeable in current building structural codes and capable of performing relevant design calculations and assessments.\n"
    "- Eligible to obtain FAA Public Trust clearance."
)

# Add a section for additional information
additional_info_heading = doc.add_heading('ADDITIONAL INFORMATION', level=1)
set_paragraph_spacing(additional_info_heading, space_before=240, space_after=120)
additional_info = doc.add_paragraph()
additional_info.add_run(
    "- Willing to relocate to Fort Worth, TX.\n"
    "- Available for 25% travel as required by the position."
)

# Save the document
output_path = 'Resume_Filled.docx'
doc.save(output_path)

print(f"Document saved as {output_path}")