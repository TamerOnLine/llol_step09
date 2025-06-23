# 🧭 Routes Documentation – llol_step09

This document explains the core route files responsible for managing resume sections, paragraphs, and fields in the project.

---

## 📁 Folder: `routes/`

This folder includes route files that define logic for handling dynamic content in a multilingual resume builder system.

---

### 1. `resume_sections.py`

#### 🔹 Purpose:
Manage **resume sections** such as "Work Experience", "Education", etc.

#### 🔧 Key Routes:
| Route | Function |
|-------|----------|
| `/sections` | List all sections |
| `/sections/add` | Add a new section |
| `/sections/edit/<id>` | Edit a section |
| `/sections/delete/<id>` | Delete a section |
| `/sections/toggle/<id>` | Toggle section visibility |
| `/sections/reorder` | Reorder sections |

#### 📌 Features:
- Supports multilingual titles via `title_translations`
- Visibility control via `is_visible`
- Section order management

---

### 2. `resume_paragraphs.py`

#### 🔹 Purpose:
Manage **paragraphs within sections** (e.g., a group of jobs under Work Experience).

#### 🔧 Key Routes:
| Route | Function |
|-------|----------|
| `/paragraphs/<section_id>` | List all paragraphs in a section |
| `/paragraphs/add/<section_id>` | Add a new paragraph |
| `/paragraphs/edit/<id>` | Edit a paragraph |
| `/paragraphs/delete/<id>` | Delete a paragraph |
| `/paragraphs/toggle/<id>` | Toggle paragraph visibility |
| `/paragraphs/reorder/<section_id>` | Reorder paragraphs |

#### 📌 Features:
- Each paragraph belongs to a section (`section_id`)
- Paragraph type via `field_type`
- Visibility and ordering supported

---

### 3. `resume_fields.py`

#### 🔹 Purpose:
Manage **individual fields** within a paragraph (e.g., one job or one skill).

#### 🔧 Key Routes:
| Route | Function |
|-------|----------|
| `/fields/<paragraph_id>` | List all fields in a paragraph |
| `/fields/add/<paragraph_id>` | Add a new field |
| `/fields/edit/<id>` | Edit a field |
| `/fields/delete/<id>` | Delete a field |
| `/fields/toggle/<id>` | Toggle field visibility |
| `/fields/reorder/<paragraph_id>` | Reorder fields |

#### 📌 Features:
- Supports multilingual values via `title_translations` and `value_translations`
- Linked to `paragraph_id`
- Visibility and ordering supported

---

## 🧠 Summary Table

| File | Manages | Depends on |
|------|---------|------------|
| `resume_sections.py` | Sections | Top-level |
| `resume_paragraphs.py` | Paragraphs | Linked to `ResumeSection` |
| `resume_fields.py` | Fields | Linked to `ResumeParagraph` |

---

This routing structure allows dynamic, ordered, and localized management of resume content in a modular fashion.