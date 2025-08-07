# Court-Data_Dashboard

# 🏛️ Court-Data Fetcher & Mini-Dashboard

This project is a web-based application that allows users to **fetch case details** and **latest judgments/orders** from the **Delhi High Court** by entering specific case information.

## 🔍 Objective

To provide a user-friendly interface for searching and viewing court case metadata and recent updates by accessing **Delhi High Court's** publicly available online services.

## 🌐 Targeted Court

- [Delhi High Court](https://delhihighcourt.nic.in/)

## ⚙️ Features

- 🔎 Search by Case Type and Case Number.
- 📄 View latest **judgments/orders** related to the case.
- 📊 Display important case **metadata**.
- 🖨️ Export results to PDF using a simple download button.

## 🏗️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Backend**: Python (Flask)
- **Web scraping**: `requests`, `BeautifulSoup`
- **PDF generation**: `reportlab`
- **Video Recording**: Screen capture
- **Browser automation**: `selenium`, `undetected-chromedriver`

## 🖥️ How It Works

1. The user selects a **case type** and enters the **case number** and **year**.
2. The app sends a request to the **Delhi High Court** website and scrapes the case metadata and latest order/judgment using BeautifulSoup.
3. The results are shown on the web dashboard.
4. A **Download PDF** button allows the user to save the details.

## 📦 Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
