import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://usj.edu.lb/ige/"
TARGET_URL = BASE_URL + "diplome.php?diplome=809&lang=2"

def get_course_details(course_url):
    """
    Scrape detailed info from individual course page.
    """
    try:
        full_url = course_url + "&lang=2"
        res = requests.get(full_url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")

        # Find main content table
        table = soup.select_one("section#main-content table.table-bordered")
        if not table:
            return {}

        rows = table.select("tbody tr")
        if len(rows) < 1:
            return {}

        # Extract main course info
        second_td = rows[0].find_all("td")[1]

        description = second_td.find("p").get_text(" ", strip=True)

        all_paragraphs = second_td.find_all("p")

        presencial_hours = None
        student_hours = None
        evaluation = None
        references = None

        for p in all_paragraphs:
            text = p.get_text(" ", strip=True)
            if "présentiel" in text:
                presencial_hours = text
            elif "Charge de travail" in text:
                student_hours = text
            elif "Méthode" in text:
                evaluation = text
            elif "Référence" in text:
                references = text.replace("Référence :", "").strip()

        return {
            "description": description,
            "presencial_hours": presencial_hours,
            "student_hours": student_hours,
            "evaluation": evaluation,
            "references": references
        }
    except Exception as e:
        print(f"❌ Error fetching course details from {course_url}: {e}")
        return {}

# Step 1: Scrape main course list
response = requests.get(TARGET_URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

course_container = soup.find("div", id="pere0")
if not course_container:
    raise Exception("Main course container (#pere0) not found.")

courses = []
current_year = None
current_semester = None

for element in course_container.descendants:
    if element.name == "div" and element.get_text(strip=True) in ["First year", "Second year"]:
        current_year = element.get_text(strip=True)

    if element.name == "span" and "Semester" in element.get_text():
        current_semester = element.get_text(strip=True)

    if element.name == "a" and "matieres.php" in element.get("href", ""):
        course_name = element.get_text(strip=True)
        course_link = BASE_URL + element["href"].replace("&amp;", "&")

        # Step 2: Scrape course detail
        print(f"🔍 Fetching: {course_name}")
        details = get_course_details(course_link)
        time.sleep(0.5)  # Be polite to server

        course_record = {
            "year": current_year,
            "semester": current_semester,
            "course_name": course_name,
            "course_url": course_link + "&lang=2",
            **details
        }
        courses.append(course_record)

# Step 3: Save all data
df = pd.DataFrame(courses)
df.to_excel("usj_course_details.xlsx", index=False)

print(f"✅ Completed! Extracted {len(df)} courses with descriptions and saved to 'usj_course_details.xlsx'")
