from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def create_cover_letter():
    # Create a new Document
    doc = Document()

    # Add the header information
    header = doc.add_paragraph()
    header.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    header_run = header.add_run("Ryan Gallagher\nMedia, PA\n(610) 731-3822\nryan.gallagher900@gmail.com")
    header_run.font.size = Pt(12)

    # Add a blank line
    doc.add_paragraph()

    # Add the date
    date_paragraph = doc.add_paragraph()
    date_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    date_run = date_paragraph.add_run("[Today's Date]")
    date_run.font.size = Pt(12)

    # Add a blank line
    doc.add_paragraph()

    # Add the recipient's information
    recipient = doc.add_paragraph()
    recipient_run = recipient.add_run("[Hiring Manager’s Name]\nLeidos\n[Company's Address]\nFort Worth, TX")
    recipient_run.font.size = Pt(12)

    # Add a blank line
    doc.add_paragraph()

    # Add the salutation
    salutation = doc.add_paragraph()
    salutation_run = salutation.add_run("Dear [Hiring Manager’s Name],")
    salutation_run.font.size = Pt(12)

    # Add a blank line
    doc.add_paragraph()

    # Add the body of the cover letter
    body = doc.add_paragraph()
    body_text = (
        "I am writing to express my interest in the Mid-level Structural Engineer / Project Engineer position "
        "(Job Number: R-00131291) posted by Leidos. With a substantial experience as a Mechanical Engineer at Leidos "
        "and a strong educational background, I believe my skills and qualifications align well with the requirements of this role and the dynamic team at the National Airspace System Integration Support Contract (NISC IV) Team.\n\n"
        "In my current role at Leidos, I have been instrumental in the design and development of autonomous systems for the U.S. Navy and DARPA unmanned surface vessels. Through my work, I have demonstrated proficiency in model development, data analysis, and the implementation of various engineering solutions which have optimized system performance and efficiency. These responsibilities have equipped me with the hands-on experience and technical knowledge required to execute the site-specific project plans, feasibility analyses, and technical support mentioned in the job listing.\n\n"
        "My experience in developing digital models and using computer-aided design tools such as AutoCAD and SolidWorks will be particularly relevant to the development of project drawings as per FAA standards. Moreover, my experience in collaborating with the Naval Surface Warfare Center on large scale projects mirrors the collaborative environment I foresee at Leidos, as indicated by the requirement for Joint Acceptance Inspections (JAI) and Contractor Acceptance Inspections (CAI).\n\n"
        "My academic background, including a Master's degree in Computer Science with a focus on artificial intelligence and machine learning, further augments my ability to create innovative solutions and leverage advanced analytical skills. My familiarity with various programming languages, libraries, and simulation tools enhances my ability to perform comprehensive site surveys, data collection, and subsequent analysis—key components of the Structural Engineer role.\n\n"
        "I am excited about the prospect of contributing to Leidos’ mission by bringing my expertise and innovative approach to the FAA Infrastructure Engineering Center. Please find my resume attached for further details on my professional journey and accomplishments.\n\n"
        "I look forward to the opportunity to discuss how my skills and experiences can be beneficial to your team. Thank you for considering my application."
    )
    body_run = body.add_run(body_text)
    body_run.font.size = Pt(12)

    # Add a blank line
    doc.add_paragraph()

    # Add the closing
    closing = doc.add_paragraph()
    closing_run = closing.add_run("Warmest regards,\n\nRyan Gallagher\nryan.gallagher900@gmail.com\n(610) 731-3822")
    closing_run.font.size = Pt(12)

    # Save the document
    doc.save("cover_letter_template_filled.docx")

create_cover_letter()