import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

from controller.InitializeButton import InitializeButton
from controller.ManageButton import ManageButton
from controller.ChallengeButton import create_challenge_button
from controller.ExitButton import create_exit_button
from controller.Leaderboard import add_leaderboard_to_main_window
from controller.RankingButton import create_ranking_button
from controller.RestartButton import create_restart_button
from controller.StatisticsButton import create_statistics_button

# Initialize main window
main_window = tk.Tk()
main_window.title("Tennis Ladder")
main_window.state("zoomed")

# Determine path to bundled or source-based assets
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller temp path
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# Load background image safely
image_path = os.path.join(base_path, "maurits-bausenhart-XtcZbSPVJ3A-unsplash.png")
background_image = ImageTk.PhotoImage(Image.open(image_path))
background_label = tk.Label(main_window, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Layout frames
button_frame = tk.Frame(main_window, bg='white', bd=2)
button_frame.pack(side="left", fill="y", pady='90')

leaderboard_frame = tk.Frame(main_window, bg="white", bd=2, width=600, height=450)
leaderboard_frame.place(relx=0.2, rely=0.1)

# Leaderboard refresh function
refresh_leaderboard = add_leaderboard_to_main_window(leaderboard_frame)

# Add buttons
restart_button = create_restart_button(button_frame)
restart_button.pack(padx=10, pady=10)

ranking_button = create_ranking_button(button_frame)
ranking_button.pack(padx=10, pady=10)

initialize_button = InitializeButton(button_frame)
initialize_button.get_button().pack(padx=10, pady=10)

manage_button = ManageButton(button_frame, refresh_leaderboard)
manage_button.pack(padx=10, pady=10)

challenge_button = create_challenge_button(button_frame, refresh_leaderboard)
challenge_button.pack(padx=10, pady=10)

statistics_button = create_statistics_button(button_frame)
statistics_button.pack(padx=10, pady=10)

exit_button = create_exit_button(button_frame, main_window)
exit_button.pack(padx=10, pady=10)

# Start GUI event loop
main_window.mainloop()
