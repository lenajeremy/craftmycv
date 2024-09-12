"""
Testing how the python-docx library works
"""
from docx import Document

document = Document("template_edited.docx")
jobs=[ 'Data Science', 'Data Engineering', 'Software Engineer', 'CEO', 'CTO']
phone_number = "08033333333"
email = "hello@gmail.com"
address = "1234 Main St, Anytown, USA"
companies=[ 'google', 'meta', 'amazon', 'BOFA', 'JP Morgan']
cities=['Lagos', 'Ibadan', 'Ikeja', 'Abuja', 'Kano']
countries=['Nigeria']*5
year_starts=['2022', '2023', '2025', '2019', '2024']
year_ends=year_starts[::-1]
expereinces=["Machines learnt"]*5


for paragraph in document.paragraphs:
    if "{FULLNAME}" in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace("{FULLNAME}", "Ambrose")
    elif "{PROFILE_SUMMARY}" in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace("{PROFILE_SUMMARY}", "Machines are still learning")
    
    for j in range(1, 6):
        if "{JOB_TITLE"+str(j)+"}" in paragraph.text:
            for run in paragraph.runs:
                run.text = run.text.replace("{JOB_TITLE"+str(j)+"}", jobs[j-1])
                run.text = run.text.replace("{COMPANY"+str(j)+"}", companies[j-1])
                run.text = run.text.replace("{CITY"+str(j)+"}", cities[j-1])
                run.text = run.text.replace("{COUNTRY"+str(j)+"}", countries[j-1])
                run.text = run.text.replace("{YEAR_START"+str(j)+"}", year_starts[j-1])
                run.text = run.text.replace("{YEAR_END"+str(j)+"}", year_ends[j-1])
                run.text = run.text.replace("{EXPERIENCE_SUMMARY"+str(j)+"}", expereinces[j-1])
    if "{PHONE_NUMBER}" in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace("{PHONE_NUMBER}", phone_number)
    if "{EMAIL_ADDRESSES}" in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace("{EMAIL_ADDRESSES}", email)
    if "{ADDRESS}" in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace("{ADDRESS}", address)

document.save(('hello.docx'))
