# ⚡ Smart Todo App

An intelligent, distraction-free productivity assistant built using **Python, SQLite, Streamlit, and Generative AI**.

This project was developed as part of the **NGK Internship Assignment**, with a focus on clean UI design, robust task management, and thoughtful AI integration.

---

## 🚀 Overview

The **Smart Todo App** goes beyond a basic to-do list.  
It helps users **organize tasks**, **track progress**, and **overcome procrastination** using AI-assisted insights — all within a modern, responsive interface.

The application is fully local (SQLite-based), privacy-safe, and does **not** expose any API keys in the source code.

---

## ✨ Key Features

### 1️⃣ Task Management
- **Detailed Task Creation**
  - Title (required)
  - Description (optional)
  - Priority (1–5)
  - Due Date
  - Time & Timezone support
- **Inline Edit Mode**
  - Edit task details directly without leaving the page
- **Status Control**
  - Mark tasks as **Done** or **Undo** with one click
- **Delete Tasks**
  - Permanently remove completed or irrelevant tasks

---

### 2️⃣ Smart Organization
- **Priority Levels**
  - Visual color indicators (Red = High, Green = Low)
- **Sorting**
  - By **Priority** (High → Low)
  - By **Due Date** (Earliest → Latest)
- **Filtering**
  - View **All**, **Pending**, or **Completed** tasks
- **Progress Bar**
  - Live visual indicator of task completion

---

### 3️⃣ Generative AI Integration
- **“Why am I stuck?” Insight**
  - Uses a Generative AI API to analyze why a task feels difficult
  - Suggests a small, actionable first step
- **Graceful Fallback**
  - If the AI quota is exceeded or unavailable, the app displays a helpful human-written tip
  - Ensures the app never crashes or exposes raw API errors

> ⚠️ **Important:**  
> API keys are read only from environment variables and are **never included in the source code**.

---

### 4️⃣ Enhanced UX & UI
- **Modern Card-Based Design**
  - Clean typography (Inter font)
  - Hover effects and soft shadows
- **Safe Input Handling**
  - Tasks are created **only** when the user clicks **“Add Task”**
  - Pressing `Enter` does not accidentally submit
- **Timezone-Aware Deadlines**
  - Designed for global usage
- **Professional Layout**
  - Clear spacing, readable contrast, and intuitive controls
- **Branded Footer**
  - Includes a clickable LinkedIn profile link

---

## 🧱 Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend:** Python  
- **Database:** SQLite  
- **AI Integration:** Gemini Generative AI API  
- **Styling:** Custom CSS (embedded in Streamlit)  

---

## 📂 Project Structure

```text
todo_app/
│
├── app.py              # Main Streamlit application
├── database.py         # SQLite database operations
├── ai_utils.py         # Generative AI logic with safe fallback
├── requirements.txt    # Python dependencies
└── tasks.db            # SQLite database (auto-created)
````

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set Environment Variable (API Key)

```bash
export GEMINI_API_KEY="your_api_key_here"      # macOS / Linux
setx GEMINI_API_KEY "your_api_key_here"        # Windows
```

### 3️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 🔒 Security & Best Practices

* ✅ No API keys committed to source code
* ✅ Graceful handling of AI quota limits
* ✅ SQLite transactions safely managed
* ✅ Clean session-state handling to avoid UI crashes

---

## 🎯 Evaluation Focus (NGK Internship)

This project demonstrates:

* Practical use of **Python, SQLite, Streamlit**
* Responsible **Generative AI integration**
* Attention to **UI/UX quality**
* Robust error handling and clean architecture

---

## 👤 Author

**Shivam Rathaur**  
Indian Institute of Technology Hyderabad  

🔗 **LinkedIn:** [https://www.linkedin.com/in/shivam-rathaur/](https://www.linkedin.com/in/shivam-rathaur/)


---

## 📜 License

This project is intended for academic and evaluation purposes as part of the NGK Internship selection process.

```

---
