from docxtpl import DocxTemplate

doc = DocxTemplate("template-1-pre.docx")

resume_data = {
    "full_name": "John Doe",
    "phone_number": "1234567890",
    "email_address": "johndoe@example.com",
    "address": "1234 Main St, Anytown, USA",
    "link": "https://www.linkedin.com/in/johndoe",
    "profile_summary": "I am a software engineer with over 5 years of experience in developing and maintaining web applications using Python and Django.",
    "education": [
        {
            "school": "University of California, Los Angeles",
            "degree": "Bachelor of Science in Computer Science",
            "start_date": "2010",
            "end_date": "2014",
            "course_studied": "Computer Science",
            "grade": "3.8"
        },
    ],
    "experience": [
        {
            "company": "Google",
            "location": "Mountain View, CA",
            "responsibilities": "Developed and maintained web applications using Python and Django",
            "role": "Software Engineer",
            "start_date": "2014",
            "end_date": "2016"
        },
        {
            "company": "Facebook",
            "location": "Menlo Park, CA",
            "responsibilities": "Developed and maintained web applications using Python and Django",
            "role": "Senior Software Engineer",
            "start_date": "2016",
            "end_date": "2018"
        },
        {
            "company": "Twitter",
            "location": "San Francisco, CA",
            "responsibilities": "Led backend development for real-time data processing pipeline, optimizing performance and scalability for millions of users.",
            "role": "Software Engineer",
            "start_date": "2018",
            "end_date": "2020"
        },
    ],
    "skills": [
        "Python",
        "Java",
        "JavaScript",
        "SQL"
    ]
}

doc.render(resume_data)
doc.save("resume-1.docx")