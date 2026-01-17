import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys
import ctypes
import time
import threading

class FloatingOSK(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window basic
        self.title("OSK Launcher")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.overrideredirect(True)

        # Set window icon (if icon.png exists)
        try:
            icon_path = self._get_resource_path("icon.png")
            if os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
                self.icon_photo = ImageTk.PhotoImage(icon_img)
                self.iconphoto(True, self.icon_photo)
        except Exception as e:
            print(f"Could not load icon: {e}")

        # Initial position
        self.geometry("140x40+50+50")

        # Styling - dark background
        bg = "#1e1e1e"
        self.configure(bg=bg)

        # Main container frame - NO PADDING
        frame = tk.Frame(self, bg=bg, bd=0, relief="flat")
        frame.pack(fill="both", expand=True)

        # Load keyboard image
        image_loaded = False
        try:
            img_path = self._get_resource_path("keyboard_image.png")
            
            if os.path.exists(img_path):
                img = Image.open(img_path)
                
                # Check if image has transparency
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    print("✓ Image has transparency")
                else:
                    print("Image does not have transparency - converting")
                    img = img.convert('RGBA')
                
                # Resize to exact button size
                img = img.resize((140, 40), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
                
                # Use Label with image - NO background parameter (lets transparency show)
                self.btn = tk.Label(
                    frame,
                    image=self.photo,
                    cursor="hand2",
                    borderwidth=0,
                    highlightthickness=0,
                    relief="flat"
                )
                image_loaded = True
                print("✓ Image loaded successfully!")
            else:
                print("✗ Image file not found")
        except Exception as e:
            print(f"✗ Could not load keyboard image: {e}")

        # Fallback to text button if image didn't load
        if not image_loaded:
            print("Using fallback text button")
            self.btn = tk.Label(
                frame,
                text="🎹 Keyboard",
                bg="#2d7dff",
                fg="white",
                cursor="hand2",
                font=("Segoe UI", 12, "bold"),
                borderwidth=0,
                highlightthickness=0
            )

        # Pack with NO padding
        self.btn.pack(fill="both", expand=True, padx=0, pady=0)

        # Right-click menu
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Exit", command=self._exit_app)

        # Drag support
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._has_moved = False

        # Bindings
        for w in (self, frame, self.btn):
            w.bind("<ButtonPress-1>", self._start_move)
            w.bind("<B1-Motion>", self._on_move)
            w.bind("<ButtonRelease-1>", self._end_move)
            w.bind("<Button-3>", self._show_menu)

        # ESC to quit
        self.bind("<Escape>", lambda e: self._exit_app())

    def _get_resource_path(self, relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

    def _start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._has_moved = False

    def _on_move(self, event):
        x = self.winfo_pointerx() - self._drag_start_x
        y = self.winfo_pointery() - self._drag_start_y
        self.geometry(f"+{x}+{y}")
        self._has_moved = True

    def _end_move(self, event):
        if not self._has_moved:
            # Launch in background thread to prevent hanging
            threading.Thread(target=launch_osk, daemon=True).start()

    def _show_menu(self, event):
        # Safety check - don't show menu if app is closing
        try:
            if self.winfo_exists():
                # Unpost any existing menu first
                self.menu.unpost()
                # Small delay to ensure clean menu display
                self.after(10, lambda: self.menu.tk_popup(event.x_root, event.y_root))
        except tk.TclError:
            pass  # App is already destroyed, ignore

    def _exit_app(self):
        """Cleanly exit the application"""
        try:
            # Unpost menu if it's showing
            self.menu.unpost()
        except:
            pass
        
        # Destroy the window
        try:
            self.quit()
            self.destroy()
        except:
            pass


def launch_osk():
    """Launch On-Screen Keyboard - FIXED to prevent hanging"""
    print("\n" + "="*60)
    print("OSK LAUNCHER")
    print("="*60)
    
    # Method 1: Try shell execution (works best, doesn't hang)
    try:
        print("\n[Method 1] Trying: Shell execution (non-blocking)")
        os.system("start osk.exe")
        print("✓ SUCCESS: OSK launched")
        return
    except Exception as e:
        print(f"✗ FAILED: Shell execution - {e}")
    
    # Method 2: Subprocess with DETACHED_PROCESS flag
    try:
        print("\n[Method 2] Trying: Detached process")
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen("osk.exe", creationflags=DETACHED_PROCESS)
        print("✓ SUCCESS: OSK launched")
        return
    except Exception as e:
        print(f"✗ FAILED: Detached process - {e}")
    
    # Method 3: Direct path with detached flag
    try:
        print("\n[Method 3] Trying: Direct path (detached)")
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(r"C:\Windows\System32\osk.exe", creationflags=DETACHED_PROCESS)
        print("✓ SUCCESS: OSK launched")
        return
    except Exception as e:
        print(f"✗ FAILED: Direct path - {e}")
    
    # Method 4: CMD wrapper
    try:
        print("\n[Method 4] Trying: CMD wrapper")
        subprocess.Popen(["cmd", "/c", "start", "osk.exe"], shell=True)
        print("✓ SUCCESS: OSK launched")
        return
    except Exception as e:
        print(f"✗ FAILED: CMD wrapper - {e}")
    
    print("\n" + "="*60)
    print("ERROR: All launch methods failed")
    print("="*60)


if __name__ == "__main__":
    app = FloatingOSK()
    app.mainloop()