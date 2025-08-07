from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fetch', methods=['POST'])
def fetch_case():
    case_type = request.form.get('case_type')
    case_number = request.form.get('case_number')
    case_year = request.form.get('case_year')

    if not case_type or not case_number or not case_year:
        return render_template("result.html", error="❌ Please fill all fields.")

    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument('--log-level=3')

    driver = webdriver.Chrome(options=options)
    driver.get("https://delhihighcourt.nic.in/app/get-case-type-status")

    try:
        wait = WebDriverWait(driver, 60)

        wait.until(EC.presence_of_element_located((By.ID, "case_type")))
        dropdown = Select(driver.find_element(By.ID, "case_type"))
        valid_options = [opt.text.strip() for opt in dropdown.options]

        if case_type not in valid_options:
            driver.quit()
            return render_template("result.html", error=f"❌ Invalid Case Type: '{case_type}'.")

        dropdown.select_by_visible_text(case_type)
        driver.find_element(By.ID, "case_number").send_keys(case_number)
        driver.find_element(By.ID, "case_year").send_keys(case_year)

        print("🔒 Please solve the CAPTCHA and click 'Submit' on the browser.")
        input("👉 Press ENTER here once the table appears on screen...")

        wait.until(lambda d: (
            d.find_element(By.ID, "caseTable").is_displayed() and
            "No data available" not in d.find_element(By.ID, "caseTable").text
        ))

        table = driver.find_element(By.ID, "caseTable")
        rows = table.find_elements(By.TAG_NAME, "tr")

        if len(rows) < 2:
            driver.quit()
            return render_template("result.html", error="❌ No matching case found.")

        columns = rows[1].find_elements(By.TAG_NAME, "td")
        parties = columns[1].text.strip() if len(columns) > 1 else "N/A"
        filing_date = columns[2].text.strip() if len(columns) > 2 else "N/A"
        next_hearing = columns[3].text.strip() if len(columns) > 3 else "N/A"

        # 🔗 STEP 1: Click on the "Orders" link if available
        pdf_links = []
        try:
            for link in driver.find_elements(By.TAG_NAME, "a"):
                if "order" in link.text.lower():
                    link.click()
                    break

            # 🔁 STEP 2: Wait for the PDF links to load in updated table
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#caseTable a")))

            # 🔍 STEP 3: Find all <a> tags that point to PDF files
            pdf_anchors = driver.find_elements(By.CSS_SELECTOR, "#caseTable a")

            for anchor in pdf_anchors:
                href = anchor.get_attribute("href")
                if href and ".pdf" in href.lower():
                    if not href.startswith("http"):
                        href = "https://delhihighcourt.nic.in" + href
                    pdf_links.append(href)

        except Exception as e:
            print("PDF link extraction error:", e)

        driver.quit()

        return render_template("result.html",
                               case_type=case_type,
                               case_number=case_number,
                               case_year=case_year,
                               parties=parties,
                               filing_date=filing_date,
                               next_hearing=next_hearing,
                               pdf_links=pdf_links)

    except Exception as e:
        driver.save_screenshot("error_screenshot.png")
        driver.quit()
        with open("error_log.txt", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        return render_template("result.html", error="❌ Error fetching details. See 'error_log.txt' or 'error_screenshot.png'.")

if __name__ == '__main__':
    app.run(debug=True)
