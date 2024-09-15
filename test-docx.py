"""
Testing how the python-docx library works
"""
from d import Document

def replace_text(doc, old_text, new_text):
    # Search and replace in paragraphs
    for para in doc.paragraphs:
        for run in para.runs:
            run.text = run.text.replace(old_text, new_text)

    # Search and replace in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:
                        run.text = run.text.replace(old_text, new_text)

    # Search and replace in text boxes and other shapes
    for shape in doc.inline_shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    run.text = run.text.replace(old_text, new_text)

def count_work_experiences(doc):
    count = 0
    
    # Search in paragraphs
    for para in doc.paragraphs:
        occurrences = para.text.count("{JOB_TITLE")
        count += occurrences
        if occurrences > 0:
            print(f"Paragraph text: {para.text}\nCount: {occurrences}\n")
    
    # Search in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                occurrences = cell.text.count("{JOB_TITLE")
                count += occurrences
                if occurrences > 0:
                    print(f"Table cell text: {cell.text}\nCount: {occurrences}\n")
                
    
    # Search in text boxes and other shapes
    for shape in doc.inline_shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                occurrences = para.text.count("{JOB_TITLE")
                count += occurrences
                if occurrences > 0:
                    print(f"Shape text: {para.text}\nCount: {occurrences}\n")
    
    # Search in headers and footers
    for section in doc.sections:
        for header in section.header.paragraphs:
            occurrences = header.text.count("{JOB_TITLE")
            count += occurrences
            if occurrences > 0:
                print(f"Header text: {header.text}\nCount: {occurrences}\n")
            
        for footer in section.footer.paragraphs:
            occurrences = footer.text.count("{JOB_TITLE")
            count += occurrences
            if occurrences > 0:
                print(f"Footer text: {footer.text}\nCount: {occurrences}\n")
    
    return count

document = Document("test.docx")

# Count existing work experiences in the document
num_experiences_in_doc = count_work_experiences(document)

print(num_experiences_in_doc)

jobs = [
    "Software Engineer",
    "Data Scientist",
    "Product Manager",
    "UX/UI Designer",
    "DevOps Engineer"
]
companies = [
    "Google",
    "Meta",
    "Amazon",
    "JP Morgan",
    "BOFA"
]
cities = [
    "San Francisco",
    "Menlo Park",
    "Seattle",
    "New York",
    "Denver"
]
countries = [
    "USA",
    "USA",
    "USA",
    "USA",
    "USA"
]
year_starts = [
    "2022",
    "2022",
    "2022",
    "2022",
    "2022"
]
year_ends = [
    "2022",
    "2022",
    "2022",
    "2022",
    "Present"
]
experiences = [
    "Working in a mid-sized public accounting firm to provide professional accounting services for individuals and business clients. Provide full range of services, include income tax preparation, audit support, preparation of financial statements, pro forma budgeting, general ledger accounting, and bank reconciliation.",
    "I assisted in the development of the search team to improve the search experience for users",
    "I built a blockchain platform that allows users to trade cryptocurrencies",
    "I designed a mobile app that allows users to track their fitness goals",
    "I enabled the company to scale its operations by 30%"
]

skills = [
    "Python",
    "Java",
    "JavaScript",
    "SQL",
    "NoSQL",
    "MongoDB",
    "PostgreSQL",
]

# Assume jobs, companies, etc. are lists of user-provided experiences
num_user_experiences = len(jobs)

# Adjust the number of replacements based on the comparison
num_replacements = min(num_experiences_in_doc, num_user_experiences)

# Define your replacements as a dictionary
replacements = {
    "{FULL_NAME}": "Jeremiah Lena",
    "{PROFILE_SUMMARY}": "Machines are still learning",
    "{PHONE_NUMBER}": "07030020887",
    "{EMAIL_ADDRESS}": "jeremiahlena13@gmail.com",
    "{ADDRESS}": "24, Ogunlana Drive, Ikoyi, Lagos",
}

# Add job-related replacements dynamically
for j in range(1, num_replacements + 1):
    replacements[f"{{JOB_TITLE{j}}}"] = jobs[j-1]
    replacements[f"{{COMPANY{j}}}"] = companies[j-1]
    replacements[f"{{CITY{j}}}"] = cities[j-1]
    replacements[f"{{COUNTRY{j}}}"] = countries[j-1]
    replacements[f"{{YEAR_START{j}}}"] = year_starts[j-1]
    replacements[f"{{YEAR_END{j}}}"] = year_ends[j-1]
    replacements[f"{{EXPERIENCE_SUMMARY{j}}}"] = experiences[j-1]



# If there are more experiences in the document than provided by the user, remove the extra ones
if num_experiences_in_doc > num_user_experiences:
    for j in range(num_user_experiences + 1, num_experiences_in_doc + 1):
        replacements[f"{{JOB_TITLE{j}}}"] = ""
        replacements[f"{{COMPANY{j}}}"] = ""
        replacements[f"{{CITY{j}}}"] = ""
        replacements[f"{{COUNTRY{j}}}"] = ""
        replacements[f"{{YEAR_START{j}}}"] = ""
        replacements[f"{{YEAR_END{j}}}"] = ""
        replacements[f"{{EXPERIENCE_SUMMARY{j}}}"] = ""

# Perform replacements
for old_text, new_text in replacements.items():
    replace_text(document, old_text, new_text)

document.save('hello.docx')
