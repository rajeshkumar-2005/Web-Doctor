# 🩺 WebDoctor

WebDoctor is a website security monitoring platform built using Flask. It helps users analyze the security of a website by performing basic security checks and providing a security score with recommendations.

## 🚀 Live Demo

https://webdoctor-1fsr.onrender.com/

## 📖 About the Project

The main objective of this project is to provide a simple way to check the security status of a website. WebDoctor scans a website for common security issues such as SSL certificate status, missing security headers, open ports, and basic SQL injection indicators. Based on the scan results, it calculates a security score and suggests improvements.

## ✨ Features

- SSL Certificate Validation
- Security Header Analysis
- Open Port Detection
- Basic SQL Injection Check
- Security Score Calculation
- Risk Classification (Low, Medium, High)
- Security Trend Graph
- Priority-Based Recommendations
- PDF Report Generation
- English & Tamil Language Support
- Scan History Storage

## 🛠️ Technologies Used

- Python
- Flask
- HTML
- CSS
- JavaScript
- Chart.js
- SQLite
- Git & GitHub
- Render

## 📂 Project Structure

```
WebDoctor/
│
├── app.py
├── scanner.py
├── db.py
├── report.py
├── agent.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── scans.db
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/rajeshkumar-2005/Web-Doctor.git
```

Move to the project folder:

```bash
cd Web-Doctor
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

## 🔍 How It Works

1. Enter the website URL.
2. The application scans the website.
3. It checks SSL, security headers, open ports, and SQL injection indicators.
4. A security score is generated.
5. The risk level is displayed.
6. Suggestions are provided to improve website security.
7. Users can download a PDF report of the scan.

## 🎯 Who Can Use This?

- Website Owners
- Developers
- Students
- Cybersecurity Learners
- Small Organizations

## 🔮 Future Improvements

- AI-based vulnerability detection
- Email notifications
- More security checks
- User authentication
- Cloud database integration

## 👨‍💻 Author

**Rajesh Kumar**

GitHub:  
https://github.com/rajeshkumar-2005

## 📄 License

This project is created for learning and educational purposes.