# llol_step08

# llol_step08 – Dynamic Resume Builder with Flask

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://www.postgresql.org/)
[![i18n](https://img.shields.io/badge/i18n-Multilingual-yellow)](https://www.transifex.com/)

[![Build](https://github.com/TamerOnLine/llol_step08/actions/workflows/main.yml/badge.svg)](https://github.com/TamerOnLine/llol_step08/actions/workflows/main.yml)
[![PostgreSQL Status](https://github.com/TamerOnLine/llol_step08/actions/workflows/postgres-check.yml/badge.svg)](https://github.com/TamerOnLine/llol_step08/actions/workflows/postgres-check.yml)
[![Tests](https://github.com/TamerOnLine/llol_step08/actions/workflows/test.yml/badge.svg)](https://github.com/TamerOnLine/llol_step08/actions/workflows/test.yml)
[![Coverage](https://codecov.io/gh/TamerOnLine/llol_step08/branch/main/graph/badge.svg)](https://codecov.io/gh/TamerOnLine/llol_step08)
[![Last Commit](https://img.shields.io/github/last-commit/TamerOnLine/llol_step08)](https://github.com/TamerOnLine/llol_step08)

[![Release](https://img.shields.io/github/v/release/TamerOnLine/llol_step08?include_prereleases)](https://github.com/TamerOnLine/llol_step08/releases)
[![License](https://img.shields.io/github/license/TamerOnLine/llol_step08)](https://github.com/TamerOnLine/llol_step08)

[![Status](https://img.shields.io/badge/status-stable-brightgreen)]()
[![Maintained](https://img.shields.io/badge/maintained-yes-success.svg)]()
[![Open Issues](https://img.shields.io/github/issues/TamerOnLine/llol_step08)](https://github.com/TamerOnLine/llol_step08/issues)
[![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/TamerOnLine/llol_step08/pulls)

[![Stars](https://img.shields.io/github/stars/TamerOnLine/llol_step08)](https://github.com/TamerOnLine/llol_step08)
[![Forks](https://img.shields.io/github/forks/TamerOnLine/llol_step08)](https://github.com/TamerOnLine/llol_step08)


---

## 📖 Overview

**llol_step09** is the seventh milestone of an open-source dynamic resume builder aimed at empowering multilingual content creation, real-time editing, and customization. It's built for developers who need structured, localized, and exportable resume content managed through a Flask-based admin interface.

---

### 📦 Clone & Setup

Follow these steps to clone the repository and set up your development environment:

```bash
git clone https://github.com/TamerOnLine/llol_step09.git  # Clone the project repository from GitHub
cd llol_step09                                            # Navigate into the project directory
python -m venv venv                                       # Create a virtual environment named 'venv'
.\venv\Scripts\Activate                                  # Activate the virtual environment (Windows CMD)
python -m pip install --upgrade pip                       # Upgrade pip to the latest version
pip install -r requirements.txt                           # Install all required dependencies
```

#### 💡 Tip
> If you're using PowerShell, replace the activation command with:
> ```powershell
> .\venv\Scripts\Activate.ps1
> ```

#### 🎬 Demo

<p align="center">
  <a href="screenshots/install.gif">
    <img src="screenshots/install.gif" alt="Quick install demo" width="600"/>
  </a>
</p>

> 📽️ The video above shows the complete setup process for the `llol_step07` repository, from cloning to installing dependencies.

---

### 🌐 Internationalization: Running the `i18n_translate` Module

To automatically generate or update translation files for your project, run the following command:

```bash
py -m main.i18n_translate
```

This module extracts translatable strings, creates `.po` files for each supported language (if they don't exist), and optionally translates them using automated tools such as `deep-translator`.

#### 📁 Output

- `translations/` folder with updated `.po` files per language.
- Automatic generation of `.pot` template file based on source code and templates.

#### 🎬 Demo

<p align="center">
  <a href="screenshots/i18n_translate.gif">
    <img src="screenshots/i18n_translate.gif" alt="i18n_translate in action" width="600"/>
  </a>
</p>

>📽️ This tool streamlines the i18n workflow by integrating extraction, translation, and file generation in a single command.

---

## 🌍 Features

- 🌐 Multi-language support using `Flask-Babel`
- 🔄 Automatic translation using `deep-translator`
- 🧾 Live editing of sections, paragraphs, and fields
- 🎛️ Admin dashboard for dynamic content management
- 🐘 PostgreSQL as the primary database
- 🎨 Ready for resume theming and customization

---

## 🧩 Database Schema

The resume structure is built dynamically using the following tables:

- `ResumeSection`: Top-level sections (e.g., Education, Work Experience)
- `ResumeParagraph`: Paragraphs under each section with `field_type`
- `ResumeField`: Key-value pairs inside each paragraph; supports multilingual content
- `Setting`: Stores design and display options as JSON
- `LanguageOption`: Manages supported languages
- `NavigationLink`: Handles sidebar/menu navigation

A ResumeSection contains multiple ResumeParagraphs, and each ResumeParagraph includes multiple ResumeFields.

---

### 🎨 Custom Styling via Settings

You can control the appearance of your resume using the admin panel:

- **Section Title Styling**: font-size, color, weight
- **Paragraph Styling**: font-size, color
- **Body Font**: custom font stack

These are stored as JSON in the `Setting` table and dynamically applied to your resume.

---

### 🗂️ Key Files

| File | Purpose |
|------|---------|
| `main_routes.py` | Public routes (home, index, language selector) |
| `admin_builder_routes.py` | Admin: section CRUD |
| `admin_paragraph.py` | Admin: paragraph CRUD |
| `admin_field.py` | Admin: field CRUD and reordering |
| `i18n_translate.py` | Auto translation and `.po` file generation |
| `run.py` | App bootstrap with DB creation |

---

### 🛠️ Database Setup & `.env` Configuration

Before running the app, you must create the target PostgreSQL database manually and configure environment variables for the connection.

#### ✅ Step 1: Create the `.env` file

In the root directory of the project, create a file named `.env` and add the following lines:

```env
DB_NAME=postgreslebenslauf
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
FLASK_DEBUG=True
```

Replace the values with your actual PostgreSQL credentials.

> 💡 **Note:** The database `postgreslebenslauf` must already exist on your PostgreSQL server. This project does **not** create the database itself — it only creates tables inside it.

---

#### ✅ Step 2: Create the PostgreSQL database (if not already created)

You can create the database using any method you prefer:

- **Using `psql` CLI**:
  ```bash
  createdb -U postgres postgreslebenslauf
  ```

- **Inside `psql` shell**:
  ```sql
  CREATE DATABASE postgreslebenslauf;
  ```

- **Using pgAdmin GUI**:
  - Open pgAdmin
  - Right-click on **Databases** → **Create** → **Database**
  - Set the name to `postgreslebenslauf` and save

---

After completing these steps, you can start the app with:

```bash
py -m run
```

This will:
- Connect to the PostgreSQL server using the credentials in `.env`.
- Expect the database `postgreslebenslauf` to already exist.
- Create required tables automatically if missing.
- Launch the Flask app in development mode with debugging enabled.

#### 🎬 Demo

<p align="center">
  <a href="screenshots/run.gif">
    <img src="screenshots/run.gif" alt="Flask app running with py -m run" width="600"/>
  </a>
</p>

> 📽️ The animation above shows how the application is launched and confirms successful connection to the database.

---

## 📂 Project Structure

```bash
main/
├── models.py
├── routes.py
├── templates/
│   └── base.html.j2
├── static/
│   └── css/resume.css
├── translations/
└── ...
```

---

## 🗺️ Roadmap

- ✅ Step 07: Translation engine + dynamic sections
- 🚧 Step 08: Admin interface for language settings (in progress)
- ⏭️ Step 09: Display resume content using a ready-made template
- 📄 Step 10: Export resume to PDF
- 🎨 Step 11: Fine-tune paragraph formatting
- 🔜 Step 12: To be determined


---

## 🧰 Built With

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-Babel](https://python-babel.github.io/flask-babel/)
- [PostgreSQL](https://www.postgresql.org/)
- [deep-translator](https://pypi.org/project/deep-translator/)

---

## 📜 License

This project is open-source under the MIT License.  
Feel free to explore and build upon it.

---

## 👨‍💻 Developer - Connect With Me

[![GitHub](https://img.shields.io/badge/GitHub-TamerOnLine-181717?style=flat&logo=github)](https://github.com/TamerOnLine)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/tameronline/)
[![YouTube](https://img.shields.io/badge/YouTube-TamerOnPi-red?style=flat&logo=youtube)](https://www.youtube.com/@mystrotamer)


By [@TamerOnLine](https://github.com/TamerOnLine)  
Under the umbrella of [Flask University](https://github.com/Flask-University)
