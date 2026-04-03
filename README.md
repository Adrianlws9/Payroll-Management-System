# 💼 Payroll Management System (Python GUI)

A **Payroll Management System with Graphical User Interface (GUI)** built using Python. This project allows users to manage employees, track attendance, calculate salaries, and generate payslips through an interactive desktop application.

---

## 🚀 Features

* 👨‍💼 Employee Management (Add, View, Update, Delete)
* 🕒 Attendance Tracking
* 💰 Payroll Calculation (Gross, Deductions, Net Salary)
* 🧾 Payslip Generation
* 🖥️ User-friendly GUI Interface
* 🗄️ SQLite Database Integration

---

## 🛠️ Tech Stack

* **Language:** Python
* **GUI Library:** Tkinter
* **Database:** SQLite
* **Libraries Used:**

  * sqlite3
  * tkinter
  * datetime

---

## 📁 Project Structure

```plaintext
payroll-management-system/
│── main.py                  # Entry point of the application
│── database.py              # Database connection and queries
│── employee_manager.py      # Employee CRUD operations
│── attendance_tracker.py    # Attendance handling
│── payroll_calculator.py    # Salary calculations
│── payslip_generator.py     # Payslip generation logic
│── gui.py                   # GUI interface (Tkinter)
│── requirements.txt         # Dependencies
│── README.md                # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Download or Clone the Project

```bash
git clone <your-repo-link>
cd payroll-management-system
```

---

### 2. Install Python

Make sure Python 3.x is installed:

```bash
python --version
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

*(Note: Tkinter usually comes pre-installed with Python)*

---

### 4. Run the Application

```bash
python main.py
```

---

## 🖥️ How the GUI Works

The application provides a simple interface with:

* 📋 **Employee Section**
  Add, update, delete, and view employee details

* 🕒 **Attendance Section**
  Record employee attendance

* 💰 **Payroll Section**
  Calculate salary based on attendance and inputs

* 🧾 **Payslip Section**
  Generate and display employee payslips

---

## 💰 Payroll Calculation Logic

```text
Gross Salary = Basic Salary + Allowances + Bonuses

Deductions:
  - Tax = 10% of Gross Salary
  - Provident Fund = 5% of Basic Salary

Net Salary = Gross Salary - Deductions
```

---

## 📌 Example Workflow

1. Add a new employee
2. Record attendance
3. Generate payroll
4. View or print payslip

---

## 🔮 Future Improvements

* 🔐 Login Authentication System
* 📄 Export Payslip as PDF
* 📊 Graphical Dashboard (charts & analytics)
* 🌐 Convert to Web App (Flask/React)
* ☁️ Cloud Database Integration

---

## 🤝 Contribution

Feel free to fork and improve this project:

* Add new features
* Improve UI design
* Optimize code

---

## 📜 License

This project is open-source and free to use for educational purposes.

---

## 👨‍💻 Author

**Adrian Lewis**
BTech Student | Aspiring Software Developer

---

## ⭐ Learning Outcomes

This project helped in understanding:

* GUI development using Tkinter
* Modular Python programming
* Database integration
* Real-world system design

---

## 📬 Feedback

Suggestions and improvements are always welcome!

---

