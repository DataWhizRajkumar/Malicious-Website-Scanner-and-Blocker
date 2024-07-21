
import customtkinter as ctk
from tkinter import messagebox, StringVar
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import validators
from urllib.parse import urlparse
import subprocess

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email):
    global generated_otp
    generated_otp = generate_otp()

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'harivuguru@gmail.com'
    app_password = 'luux wrmh inmi rmgd'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = 'Your OTP Code'

    body = f'Your OTP code is {generated_otp}'
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        text = message.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        result.set('OTP sent successfully!')
    except Exception as e:
        result.set(f'Failed to send OTP. Error: {str(e)}')

    main_window.after(5000, clear_result)

def verify_otp():
    entered_otp = otp_entry.get()
    if entered_otp == generated_otp:
        main_window.destroy()
        open_root_window()
    else:
        result.set('Invalid OTP. Please try again.')
        main_window.after(3000, clear_result)

def clear_result():
    result.set('')

def scan_url():
    url = url_entry.get()

    if not url:
        result.set('Please enter the URL')
        root.after(3000, clear_result)
        return
    if not validators.url(url):
        messagebox.showerror(title='Invalid URL', message='Invalid URL')
        return

    api_key = 'db65295a80f627522a06f181d7fdae50e253e3136e294c59dd927f797741f255'
    params = {'apikey': api_key, 'resource': url}
    response = requests.get('https://www.virustotal.com/vtapi/v2/url/report', params=params)
    result_json = response.json()

    if 'positives' in result_json and result_json['positives'] > 0:
        result.set("Malicious URL detected!")
    else:
        result.set("URL is safe.")

    root.after(5000, clear_result)

def block_url():
    url = url_entry.get()

    if not url:
        result.set('Please enter the URL')
        root.after(3000, clear_result)
        return
    if not validators.url(url):
        messagebox.showerror(title='Invalid URL', message='Invalid URL')
        return

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if not domain:
        result.set('Invalid URL')
        root.after(3000, clear_result)
        return

    hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"

    try:
        with open(hosts_path, 'r+') as hosts_file:
            lines = hosts_file.readlines()
            hosts_file.seek(0)
            for line in lines:
                if line.strip().endswith(domain):
                    continue
                hosts_file.write(line)
            hosts_file.write(f"127.0.0.1 {domain}\n")
        subprocess.run(["ipconfig", "/flushdns"], shell=True)
        result.set(f"Blocked URL: {domain}")
    except PermissionError:
        result.set("Permission denied. Please run as administrator.")

    root.after(5000, clear_result)

def unblock_url():
    url = url_entry.get()

    if not url:
        result.set('Please enter the URL')
        root.after(3000, clear_result)
        return
    if not validators.url(url):
        messagebox.showerror(title='Invalid URL', message='Invalid URL')
        return

    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if not domain:
        result.set('Invalid URL')
        root.after(3000, clear_result)
        return

    hosts_path = "C:\\Windows\\System32\\drivers\\etc\\hosts"

    try:
        with open(hosts_path, 'r') as hosts_file:
            lines = hosts_file.readlines()

        with open(hosts_path, 'w') as hosts_file:
            for line in lines:
                if line.strip().endswith(domain):
                    continue
                hosts_file.write(line)
        subprocess.run(["ipconfig", "/flushdns"], shell=True)
        result.set(f"Unblocked URL: {domain}")
    except PermissionError:
        result.set("Permission denied. Please run as administrator.")

    root.after(5000, clear_result)

def open_root_window():
    global root
    root = ctk.CTk()
    root.title("Malicious Website Scanner and Blocker")
    root.geometry('500x400')

    main_frame = ctk.CTkFrame(root, corner_radius=10)
    main_frame.pack(expand=True, anchor='center', padx=10, pady=10)

    title_label = ctk.CTkLabel(main_frame, text="URL Safety Manager", font=('Arial', 24, 'bold'))
    entry_label = ctk.CTkLabel(main_frame, text="Enter URL:", font=('Arial', 14))
    global url_entry
    url_entry = ctk.CTkEntry(main_frame, font=('Arial', 14))
    scan_button = ctk.CTkButton(main_frame, text="Scan URL", font=('Arial', 14, 'bold'), command=scan_url)
    block_button = ctk.CTkButton(main_frame, text="Block URL", font=('Arial', 14, 'bold'), command=block_url)
    unblock_button = ctk.CTkButton(main_frame, text="Unblock URL", font=('Arial', 14, 'bold'), command=unblock_url)
    global result
    result = StringVar()
    result_label = ctk.CTkLabel(main_frame, textvariable=result, font=('Arial', 12, 'italic'))

    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))
    entry_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky='e')
    url_entry.grid(row=1, column=1, padx=(10, 20), pady=10, sticky='ew')
    scan_button.grid(row=2, column=0, columnspan=2, padx=20, pady=10)
    block_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
    unblock_button.grid(row=4, column=0, columnspan=2, padx=20, pady=10)
    result_label.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 20), sticky='ew')

    root.mainloop()


main_window = ctk.CTk()
main_window.title("OTP Verification")
main_window.geometry('500x400')

main_frame = ctk.CTkFrame(main_window, corner_radius=10)
main_frame.pack(expand=True, anchor='center', padx=10, pady=10)

email_label = ctk.CTkLabel(main_frame, text="Enter your email:", font=('Arial', 14))
email_entry = ctk.CTkEntry(main_frame, font=('Arial', 14))
otp_button = ctk.CTkButton(main_frame, text="Send OTP", font=('Arial', 14, 'bold'), command=lambda: send_otp(email_entry.get()))
otp_label = ctk.CTkLabel(main_frame, text="Enter OTP:", font=('Arial', 14))
otp_entry = ctk.CTkEntry(main_frame, font=('Arial', 14))
verify_button = ctk.CTkButton(main_frame, text="Verify OTP", font=('Arial', 14, 'bold'), command=verify_otp)
result = StringVar()
result_label = ctk.CTkLabel(main_frame, textvariable=result, font=('Arial', 12, 'italic'))

email_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky='e')
email_entry.grid(row=0, column=1, padx=(10, 20), pady=10, sticky='ew')
otp_button.grid(row=1, column=0, columnspan=2, padx=20, pady=10)
otp_label.grid(row=2, column=0, padx=(20, 10), pady=10, sticky='e')
otp_entry.grid(row=2, column=1, padx=(10, 20), pady=10, sticky='ew')
verify_button.grid(row=3, column=0, columnspan=2, padx=20, pady=10)
result_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 20), sticky='ew')

main_window.mainloop()


