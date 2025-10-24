import os
import sys
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image, ImageTk
from Dashboard import Dashboard
from Database import Database


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS  # Temp folder for bundled assets
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class App(ctk.CTk):
    ctk.set_window_scaling(1.0)
    ctk.set_widget_scaling(1.0)

    def __init__(self):
        super().__init__()
        self.title("LOGIN")
        self.geometry("400x550")
        self.resizable(False, False)
        self.config(background="#590d22")
        try:
            icon_path = resource_path("Assets/Ideal-College.ico")
            self.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting icon: {e}")
        self.create_widgets()
        self.center()

    def center(self):
        # FIXED: Proper center calculation
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 550
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    def create_widgets(self):
        self.load_images()

        # Configure main window grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Logo row
        self.grid_rowconfigure(1, weight=1)  # Login frame row

        # Logo label (centered at the top)
        self.logo_img = ctk.CTkLabel(
            self, text="", image=self.logo, text_color="white", fg_color="#590d22"
        )
        self.logo_img.grid(row=0, column=0, pady=(20, 10))

        # Login frame (centered below the logo)
        self.login_frame = ctk.CTkFrame(
            self,
            width=300,
            height=300,
            corner_radius=30,
            bg_color="#590d22",
            fg_color="#800f2f",
        )
        self.login_frame.grid(row=1, column=0, padx=50, pady=20, sticky="n")

        # Configure login frame grid for vertical alignment
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)

        # Login label (centered at the top of the frame)
        self.login_label = ctk.CTkLabel(
            self.login_frame,
            text="LOGIN",
            font=("Segoe UI", 15, "bold"),
            text_color="white",
        )
        self.login_label.grid(row=0, column=0, pady=(20, 10))

        # Username label
        self.username_label = ctk.CTkLabel(
            self.login_frame,
            text="Username",
            text_color="white",
            font=("Segoe UI", 15, "bold"),
        )
        self.username_label.grid(
            row=1, column=0, pady=(10, 0), sticky="w", padx=30)

        # Username entry
        self.username_enty = ctk.CTkEntry(
            self.login_frame,
            width=230,
            fg_color="#590d22",
            border_color="#590d22",
            text_color="white",
            height=35,
            corner_radius=20,
            font=("Segoe UI", 15, "bold"),
        )
        self.username_enty.grid(row=2, column=0, padx=30,
                                pady=(5, 10), sticky="ew")

        # Password label
        self.password_label = ctk.CTkLabel(
            self.login_frame,
            text="Password",
            text_color="white",
            font=("Segoe UI", 15, "bold"),
        )
        self.password_label.grid(
            row=3, column=0, pady=(10, 0), sticky="w", padx=30)

        # Password entry
        self.password_entry = ctk.CTkEntry(
            self.login_frame,
            width=230,
            text_color="white",
            fg_color="#590d22",
            border_color="#590d22",
            height=35,
            corner_radius=20,
            show="*",
            font=("Segoe UI", 15, "bold"),
        )
        self.password_entry.grid(
            row=4, column=0, padx=30, pady=(5, 10), sticky="ew")

        # Login button with increased bottom padding
        self.login_btn = ctk.CTkButton(
            self.login_frame,
            text="Login",
            fg_color="#590d22",
            hover_color="#a4133c",
            cursor="hand2",
            width=230,
            font=("Segoe UI", 15, "bold"),
            height=35,
            corner_radius=20,
            command=self.authentication,
        )
        self.login_btn.grid(row=5, column=0, padx=30, pady=(10, 40))

    def authentication(self):
        username = self.username_enty.get()
        password = self.password_entry.get()
        if Database.authenticate(username, password):
            self.withdraw()
            self.dashboard_window = Dashboard(self)
            self.dashboard_window.protocol(
                "WM_DELETE_WINDOW", self.on_dashboard_close)
        else:
            CTkMessagebox(
                title="Info",
                message="Invalid Credentials Please Check!",
                icon="warning",
            )

    def on_dashboard_close(self):
        if self.dashboard_window:
            self.dashboard_window.destroy()
        self.quit()

    def load_images(self):
        img_path = resource_path("Assets/Ideal-College.png")
        img = Image.open(img_path).resize((280, 190))
        self.logo = ImageTk.PhotoImage(img)


if __name__ == "__main__":
    app = App()
    app.mainloop()
