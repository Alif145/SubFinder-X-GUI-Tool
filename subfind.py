import requests
import customtkinter as ctk
from tkinter import messagebox

# Function to fetch subdomains
def fetch_subdomains():
    web = entry.get().strip()
    if not web:
        messagebox.showwarning("Input Error", "Please enter a target website.")
        return
    
    web = web.replace("https://", "").replace("http://", "").replace("/", "")
    api = f"https://api.hackertarget.com/hostsearch/?q={web}"
    
    fetch_button.configure(state="disabled", text="Fetching...")
    root.update()
    
    try:
        res = requests.get(api, timeout=10)
        if res.status_code == 200:
            subdomains = res.text.strip()
            result_text.delete("1.0", ctk.END)
            result_text.insert(ctk.END, subdomains)
        else:
            messagebox.showerror("Error", "Request failed. Please try again.")
    except requests.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")
    finally:
        fetch_button.configure(state="normal", text="Find Subdomains")

# Function to copy results to clipboard
def copy_to_clipboard():
    text = result_text.get("1.0", ctk.END).strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        messagebox.showinfo("Copied", "Results copied to clipboard.")
    else:
        messagebox.showwarning("Warning", "No results to copy.")

# Function to toggle full-screen mode
def toggle_fullscreen():
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Function to restore window size after unmaximizing
def save_geometry(event=None):
    global last_geometry
    if not root.attributes("-zoomed"):
        last_geometry = root.geometry()

def restore_geometry():
    global last_geometry
    if last_geometry:
        root.geometry(last_geometry)

# GUI Setup with customtkinter
ctk.set_appearance_mode("Dark")  # Dark mode
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("SubfinderX")
root.geometry("600x450")
root.resizable(True, True)  # Enable maximize button
last_geometry = root.geometry()  # Store initial size

root.bind("<Configure>", save_geometry)  # Track window resize

# Styling and layout
frame = ctk.CTkFrame(root, corner_radius=15)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Enter Target Website:", font=("Arial", 16)).pack(pady=10)
entry = ctk.CTkEntry(frame, width=400, height=35, font=("Arial", 14))
entry.pack(pady=5)

fetch_button = ctk.CTkButton(frame, text="Find Subdomains", command=fetch_subdomains, fg_color="#1f6aa5", hover_color="#155d8b", font=("Arial", 14))
fetch_button.pack(pady=10)

result_text = ctk.CTkTextbox(frame, width=500, height=200, font=("Arial", 12))
result_text.pack(pady=5)

copy_button = ctk.CTkButton(frame, text="Copy to Clipboard", command=copy_to_clipboard, fg_color="#1f6aa5", hover_color="#155d8b", font=("Arial", 14))
copy_button.pack(pady=10)

fullscreen_button = ctk.CTkButton(frame, text="Toggle Fullscreen", command=toggle_fullscreen, fg_color="#1f6aa5", hover_color="#155d8b", font=("Arial", 14))
fullscreen_button.pack(pady=10)

restore_button = ctk.CTkButton(frame, text="Restore Window Size", command=restore_geometry, fg_color="#1f6aa5", hover_color="#155d8b", font=("Arial", 14))
restore_button.pack(pady=10)

root.mainloop()
