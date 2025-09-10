import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "https://www.usj.edu.lb/fs/"
diploma_urls = [
    "https://usj.edu.lb/ige/diplome.php?diplome=809&lang=2",
    "https://usj.edu.lb/ige/diplome.php?diplome=808&lang=2",
    "https://www.usj.edu.lb/fs/diplome.php?diplome=192#",
    "https://www.usj.edu.lb/fs/diplome.php?diplome=935&lang=2",
    "https://www.usj.edu.lb/fs/diplome.php?diplome=1033&lang=2"
]

def get_course_details(course_url):
    # your existing function, maybe with minor tweaks
    try:
        full_url = course_url + "&lang=2" if "?lang=2" not in course_url else course_url
        res = requests.get(full_url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("section#main-content table.table-bordered")
        if not table:
            return {}

        rows = table.select("tbody tr")
        if len(rows) < 1:
            return {}

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

def scrape_diploma_page(diploma_url):
    print(f"🔍 Processing diploma page: {diploma_url}")
    response = requests.get(diploma_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    parcours = []
    # Extract parcours names and ids
    parcours_buttons = soup.select("div.div_parcours ul.tab_button_container li.tab_button")
    for btn in parcours_buttons:
        parcours_name = btn.find("strong").text.strip()
        parcours_id = btn["id"].replace("pbutton", "")  # e.g. '0', '1', '2' ...
        parcours.append({"name": parcours_name, "id": parcours_id})

    all_courses = []

    for p in parcours:
        print(f"  - Scraping {p['name']} (id {p['id']})")
        # The parcours course container divs seem to have id="pereX"
        container_id = f"pere{p['id']}"
        parcours_container = soup.find("div", id=container_id)
        if not parcours_container:
            print(f"    ❌ No container found for parcours id {p['id']}")
            continue

        # Inside this container, find all course links
        for a in parcours_container.find_all("a", href=True):
            href = a['href']
            if "matieres.php" in href:
                course_name = a.get_text(strip=True)
                course_url = BASE_URL + href.replace("&amp;", "&")
                print(f"    ▶ Found course: {course_name}")

                # Get details
                details = get_course_details(course_url)
                time.sleep(0.5)  # politeness

                course_record = {
                    "parcours": p["name"],
                    "course_name": course_name,
                    "course_url": course_url,
                    **details
                }
                all_courses.append(course_record)

    return all_courses

# Collect all courses from all diplomas
all_data = []
for url in diploma_urls:
    all_data.extend(scrape_diploma_page(url))

# Save to Excel
df = pd.DataFrame(all_data)
df.to_excel("usj_all_diploma_courses.xlsx", index=False)
print(f"✅ Done. Total courses scraped: {len(df)}")
