import tkinter as tk
from tkinter import messagebox

from DBInit import DBInit

def create_restart_button(parent_frame):
    def restart_action():
        try:
            db_init_initialization_for_restart_button = DBInit()
            restart_execution_of_database = db_init_initialization_for_restart_button.restart_db
            response = messagebox.askyesno("Restart Database","Are you sure you want to restart the Tournament?")
            if response == True:
                restart_execution_of_database()
                messagebox.showinfo("Restarted", "Restarted Completed. Activation of new Tournament!")
        except Exception as e:
            messagebox.showinfo("Error in Restart",f"Error: {e}")

    restart_button = tk.Button(
        parent_frame,
        text="Restart",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        bd=0,
        relief="solid",
        activebackground="#45a049",
        activeforeground="white",
        command=restart_action,
    )
    return restart_button
#