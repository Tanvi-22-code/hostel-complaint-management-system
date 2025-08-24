# 🏠 Hostel Complaint Management System  

A **web-based complaint management system** built with **Flask, MySQL, Pandas, and Excel**.  
This project helps hostel residents easily **register complaints**, and allows admins to **view, edit, and delete** them.  
It also supports **automatic syncing of complaints from MySQL into Excel** for offline records.  

---

## ✨ Features  
- 📝 Add complaints with username, room number, category, description, and priority  
- 📋 View all complaints in a table format  
- ✏️ Edit existing complaints  
- ❌ Delete complaints  
- 📂 Complaint categories: Electrical, Furniture, Security, Ragging, Plumbing, Cleaning, Internet, Other  
- 🔄 Auto-sync from **MySQL → Excel (`complaints.xlsx`)**  
- 🎨 Modern interface with **Tailwind CSS + Lucide Icons**  

---

## 🛠 Tech Stack  
- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Backend:** Flask (Python)  
- **Database:** MySQL  
- **Data Export:** Excel (via Pandas + OpenPyXL)  

---

## 📂 Project Structure  
hostel-complaint-management-system/


│── app.py # Main Flask application


│── requirements.txt # Python dependencies


│── .gitignore # Ignore rules


│── README.md # Project documentation


│── database.sql # MySQL schema


│── complaints.xlsx # Excel file (auto-generated)


│── templates/


│ ├── index.html # Add & View complaints


│ ├── edit.html # Edit complaint page


---

## 🚀 Future Improvements  
- Add user authentication (Admin / Student)  
- Track complaint status (Pending, Resolved)  
- Notifications (Email/SMS) for updates  
- Deployment on **Render / PythonAnywhere / Heroku**  

---

## 👨‍💻 Author  
**Tanvi Mahajan**  
📧 tanvimahajan2005@gmail.com 
🔗 [GitHub](https://github.com/Tanvi-22-code) | [LinkedIn](https://linkedin.com/in/tanvi-s-mahajan)
