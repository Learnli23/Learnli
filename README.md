**README.md for LearnLi Open Source Project**

About LearnLi 
LearnLi is a **digital learning platform** that allows students, teachers, and institutions to create, share, and access educational content. It supports **courses, eBooks, exams, and a content moderation system**, making online education **affordable, flexible, and accessible**.  

This open-source version of LearnLi allows developers, educators, and organizations to contribute and extend its capabilities.  

---

## 🌟 Features  
✅ **Course & Lesson Management** – Teachers can create structured courses with videos, notes, and assessments.  
✅ **EBook Reader with AI Assistant** – Users can read books section by section with an AI-powered reading assistant.  
✅ **Exam Registration & Management** – Students can register for exams from teachers they follow.  
✅ **Subscription System** – A flexible model allowing users to subscribe for different durations.  
✅ **Content Moderation** – Ensuring quality and compliance with community standards.  
✅ **Django & PostgreSQL Backend** – Secure, scalable, and optimized for educational content.  
✅ **Secure Payment Integration** – Powered by **Flutterwave** for seamless transactions.  

---

## 🚀 Getting Started  

### **1️⃣ Prerequisites**  
Ensure you have the following installed on your system:  
- Python **3.9+**  
- Django **4.0+**  
- PostgreSQL (or SQLite for local testing)  
- Git  
- Virtual environment tool (venv or pipenv)  

### **2️⃣ Clone the Repository**  
```sh
git clone https://github.com/Learnli23/learnli.git
cd learnli
```

### **3️⃣ Set Up Virtual Environment**  
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **4️⃣ Install Dependencies**  
```sh
pip install -r requirements.txt
```

### **5️⃣ Configure Environment Variables**  
Create a `.env` file and add:  
```env
SECRET_KEY=your-secret-key  
DEBUG=True  
DATABASE_URL=your-database-url  
FLUTTERWAVE_PUBLIC_KEY=your-public-key  
FLUTTERWAVE_SECRET_KEY=your-secret-key  
```

### **6️⃣ Apply Migrations & Create Superuser**  
```sh
python manage.py migrate
python manage.py createsuperuser
```

### **7️⃣ Run the Development Server**  
```sh
python manage.py runserver
```
Access **LearnLi** at: `http://127.0.0.1:8000/`

---

## 🛠️ Deployment Guide  
LearnLi can be deployed on platforms like **Railway, AWS, or DigitalOcean**. See [DEPLOYMENT.md](https://docs.vendure.io/) for step-by-step deployment instructions.  

---

## 🤝 Contributing  

We welcome contributions from developers, educators, and organizations. Follow these steps:  

1. **Fork the repository**  
2. **Create a feature branch**  
   ```sh
   git checkout -b feature-new-feature
   ```
3. **Make changes and commit**  
   ```sh
   git add .
   git commit -m "Added a new feature"
   ```
4. **Push to your fork and create a Pull Request**  
   ```sh
   git push origin feature-new-feature
   ```
5. **Wait for review and approval** 🎉  

---

## 🔐 Security & Best Practices  

- **DO NOT** commit secrets (e.g., API keys, database credentials).  
- Use **`.gitignore`** to exclude `venv/`, `.env`, and database dumps.  
- Regularly update dependencies to patch vulnerabilities.  

---

## 📜 License  

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.  

---

## 🎯 Contact & Support  

For discussions, issues, or feature requests, please open a GitHub **Issue** or reach out via:  

📩 Email: **learnli759@gmail.com**  
🌐 Website: [https://learnlii.com](https://learnlii.com)  
**Happy Learning!**  
 
 
