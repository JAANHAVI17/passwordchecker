import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import pyperclip
import threading
import time
from checker import PasswordChecker, PasswordStrength

class PasswordCheckerApp:
    def __init__(self, root):
        self.root = root
        self.theme_icon = None
        self.logo_img = None
        
        # Initialize all required methods in order
        self.load_assets()
        self.setup_window()
        self.create_widgets()
        self.set_theme("dark")  # Default theme
        
    def load_assets(self):
        """Load images with error handling"""
        try:
            theme_img = Image.open("assets/theme_icon.png").resize((20, 20))
            self.theme_icon = ImageTk.PhotoImage(theme_img)
        except:
            self.theme_icon = None
            
        try:
            logo_img = Image.open("assets/logo.png").resize((100, 100))
            self.logo_img = ImageTk.PhotoImage(logo_img)
        except:
            self.logo_img = None
    
    def setup_window(self):
        self.root.title("Password Checker")
        self.root.geometry("600x650")
        self.root.minsize(500, 600)
        self.root.configure(bg="#2d2d2d")
        
        # Custom title bar
        self.title_bar = tk.Frame(self.root, bg="#1e1e1e", height=40)
        self.title_bar.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.title_bar, 
            text="Password Checker", 
            bg="#1e1e1e", 
            fg="white",
            font=("Segoe UI", 10, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Theme toggle button
        if self.theme_icon:
            self.theme_btn = tk.Button(
                self.title_bar,
                image=self.theme_icon,
                command=self.toggle_theme,
                bd=0,
                bg="#1e1e1e",
                activebackground="#1e1e1e"
            )
        else:
            self.theme_btn = tk.Button(
                self.title_bar,
                text="☀/☾",
                command=self.toggle_theme,
                bd=0,
                bg="#1e1e1e",
                fg="white",
                activebackground="#1e1e1e"
            )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
    
    def create_widgets(self):
        # Main container
        self.main_frame = tk.Frame(self.root, bg="#2d2d2d", padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo
        if self.logo_img:
            logo_label = tk.Label(self.main_frame, image=self.logo_img, bg="#2d2d2d")
            logo_label.pack(pady=(0, 20))
        
        # Password Entry
        entry_frame = tk.Frame(self.main_frame, bg="#2d2d2d")
        entry_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(
            entry_frame, 
            text="Enter Password:", 
            bg="#2d2d2d", 
            fg="white",
            font=("Segoe UI", 10)
        ).pack(anchor=tk.W)
        
        self.password_entry = tk.Entry(
            entry_frame,
            font=("Segoe UI", 12),
            bd=0,
            show="•",
            bg="#3d3d3d",
            fg="white",
            insertbackground="white",
            relief=tk.FLAT,
            highlightthickness=2,
            highlightbackground="#4d4d4d",
            highlightcolor="#646cff"
        )
        self.password_entry.pack(fill=tk.X, pady=5, ipady=8)
        self.password_entry.bind("<KeyRelease>", self.check_password)
        
        # Show/Hide toggle
        self.show_password = tk.BooleanVar(value=False)
        show_btn = tk.Checkbutton(
            entry_frame,
            text="Show Password",
            variable=self.show_password,
            command=self.toggle_password_visibility,
            bg="#2d2d2d",
            fg="white",
            activebackground="#2d2d2d",
            activeforeground="white",
            selectcolor="#2d2d2d"
        )
        show_btn.pack(anchor=tk.E)
        
        # Strength Meter
        self.strength_frame = tk.Frame(self.main_frame, bg="#2d2d2d")
        self.strength_frame.pack(fill=tk.X, pady=(20, 10))
        
        self.strength_label = tk.Label(
            self.strength_frame,
            text="STRENGTH: UNKNOWN",
            bg="#2d2d2d",
            fg="#aaaaaa",
            font=("Segoe UI", 9, "bold")
        )
        self.strength_label.pack(anchor=tk.W)
        
        self.strength_meter = tk.Canvas(
            self.strength_frame,
            height=8,
            bg="#3d3d3d",
            highlightthickness=0
        )
        self.strength_meter.pack(fill=tk.X, pady=5)
        self.meter_progress = self.strength_meter.create_rectangle(
            0, 0, 0, 8, 
            fill="#ff5555", 
            outline=""
        )
        
        # Check Results
        self.results_frame = tk.LabelFrame(
            self.main_frame,
            text="Password Requirements",
            bg="#2d2d2d",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            bd=1,
            highlightbackground="#4d4d4d"
        )
        self.results_frame.pack(fill=tk.BOTH, pady=10, ipady=5, ipadx=5)
        
        # Buttons Frame
        btn_frame = tk.Frame(self.main_frame, bg="#2d2d2d")
        btn_frame.pack(fill=tk.X, pady=20)
        
        # Generate Button
        self.generate_btn = tk.Button(
            btn_frame,
            text="🔑 Generate Strong Password",
            command=self.generate_password,
            bg="#646cff",
            fg="white",
            activebackground="#747cff",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            font=("Segoe UI", 10, "bold")
        )
        self.generate_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Copy Button
        self.copy_btn = tk.Button(
            btn_frame,
            text="⎘ Copy to Clipboard",
            command=self.copy_to_clipboard,
            bg="#4d4d4d",
            fg="white",
            activebackground="#5d5d5d",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            font=("Segoe UI", 10)
        )
        self.copy_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    def toggle_password_visibility(self):
        """Toggle password visibility"""
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="•")
    
    def check_password(self, event=None):
        """Check and display password strength"""
        password = self.password_entry.get()
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        if not password:
            self.strength_label.config(text="STRENGTH: UNKNOWN", fg="#aaaaaa")
            self.strength_meter.coords(self.meter_progress, 0, 0, 0, 8)
            return
            
        strength, checks = PasswordChecker.check_strength(password)
        
        # Update strength meter with animation
        self.animate_meter(strength)
        
        # Update check results
        for rule, passed in checks.items():
            frame = tk.Frame(self.results_frame, bg="#3d3d3d")
            frame.pack(fill=tk.X, pady=2, padx=5)
            
            icon = "✓" if passed else "✗"
            color = "#4CAF50" if passed else "#F44336"
            
            tk.Label(
                frame,
                text=icon,
                fg=color,
                bg="#3d3d3d",
                font=("Segoe UI", 10, "bold")
            ).pack(side=tk.LEFT, padx=5)
            
            tk.Label(
                frame,
                text=rule,
                fg="white" if passed else "#aaaaaa",
                bg="#3d3d3d",
                font=("Segoe UI", 9)
            ).pack(side=tk.LEFT)
    
    def animate_meter(self, strength):
        """Animate the strength meter"""
        target_width = {
            PasswordStrength.WEAK: 0.25,
            PasswordStrength.MEDIUM: 0.5,
            PasswordStrength.STRONG: 0.75,
            PasswordStrength.VERY_STRONG: 1
        }[strength]
        
        colors = {
            PasswordStrength.WEAK: "#ff5555",
            PasswordStrength.MEDIUM: "#ffbb33",
            PasswordStrength.STRONG: "#4CAF50",
            PasswordStrength.VERY_STRONG: "#2196F3"
        }
        
        self.strength_label.config(
            text=f"STRENGTH: {strength.name.replace('_', ' ')}",
            fg=colors[strength]
        )
        
        meter_width = self.strength_meter.winfo_width()
        final_width = meter_width * target_width
        
        def animation():
            current = 0
            while current < final_width:
                current += meter_width * 0.05
                if current > final_width:
                    current = final_width
                self.strength_meter.coords(self.meter_progress, 0, 0, current, 8)
                self.strength_meter.itemconfig(self.meter_progress, fill=colors[strength])
                self.root.update()
                time.sleep(0.02)
                
        threading.Thread(target=animation, daemon=True).start()
    
    def generate_password(self):
        """Generate and display a strong password"""
        password = PasswordChecker.generate_strong_password()
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.check_password()
        
        # Flash the generate button for feedback
        self.flash_button(self.generate_btn, "#aaccff", "#646cff")
        
        # Show success message
        self.show_tooltip(self.generate_btn, "Password Generated!")
    
    def copy_to_clipboard(self):
        """Copy password to clipboard"""
        password = self.password_entry.get()
        if password:
            pyperclip.copy(password)
            
            # Flash the copy button for feedback
            self.flash_button(self.copy_btn, "#aaccff", "#4d4d4d")
            
            # Show success message
            self.show_tooltip(self.copy_btn, "Copied to Clipboard!")
        else:
            messagebox.showwarning("Empty Password", "No password to copy")
    
    def flash_button(self, button, flash_color, original_color):
        """Flash a button to show action feedback"""
        button.config(bg=flash_color)
        self.root.after(200, lambda: button.config(bg=original_color))
    
    def show_tooltip(self, widget, message):
        """Show a temporary tooltip near a widget"""
        x, y = widget.winfo_rootx(), widget.winfo_rooty()
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x+30}+{y-30}")
        label = tk.Label(
            tooltip, 
            text=message, 
            bg="#646cff", 
            fg="white",
            padx=10, 
            pady=5,
            font=("Segoe UI", 8)
        )
        label.pack()
        self.root.after(1000, tooltip.destroy)
    
    def toggle_theme(self):
        """Toggle between dark and light theme"""
        if self.root.cget("bg") == "#2d2d2d":
            self.set_theme("light")
        else:
            self.set_theme("dark")
    
    def set_theme(self, theme):
        """Set the color theme for the application"""
        if theme == "dark":
            colors = {
                "bg": "#2d2d2d",
                "fg": "white",
                "entry_bg": "#3d3d3d",
                "highlight": "#646cff",
                "title_bg": "#1e1e1e",
                "results_bg": "#3d3d3d",
                "meter_bg": "#3d3d3d",
                "btn_bg": "#4d4d4d",
                "gen_btn_bg": "#646cff"
            }
        else:
            colors = {
                "bg": "#f5f5f5",
                "fg": "#333333",
                "entry_bg": "white",
                "highlight": "#646cff",
                "title_bg": "#e0e0e0",
                "results_bg": "#ffffff",
                "meter_bg": "#e0e0e0",
                "btn_bg": "#d0d0d0",
                "gen_btn_bg": "#646cff"
            }
        
        # Update all widgets
        self.root.config(bg=colors["bg"])
        self.title_bar.config(bg=colors["title_bg"])
        self.title_label.config(bg=colors["title_bg"], fg=colors["fg"])
        self.main_frame.config(bg=colors["bg"])
        self.password_entry.config(
            bg=colors["entry_bg"], 
            fg=colors["fg"],
            highlightbackground="#d0d0d0" if theme == "light" else "#4d4d4d",
            highlightcolor=colors["highlight"]
        )
        self.strength_frame.config(bg=colors["bg"])
        self.strength_label.config(bg=colors["bg"], fg=colors["fg"])
        self.strength_meter.config(bg=colors["meter_bg"])
        self.results_frame.config(
            bg=colors["bg"],
            fg=colors["fg"],
            highlightbackground="#d0d0d0" if theme == "light" else "#4d4d4d"
        )
        
        # Update buttons
        self.copy_btn.config(
            bg=colors["btn_bg"],
            activebackground="#5d5d5d" if theme == "dark" else "#e0e0e0"
        )
        self.generate_btn.config(
            bg=colors["gen_btn_bg"],
            activebackground="#747cff"
        )
        
        # Update all children in results frame
        for widget in self.results_frame.winfo_children():
            widget.config(bg=colors["results_bg"])
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=colors["results_bg"])

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordCheckerApp(root)
    root.mainloop()