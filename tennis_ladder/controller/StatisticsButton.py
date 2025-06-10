import tkinter as tk
from tkinter import messagebox

from controller.ChallengeButton import connection_services_challenge_button

(player_service, db_utils_for_statistics, db_init_for_statistics,
 session_for_statistics, match_repository, player_repository_for_statistics,
 league_round_repository, match_service) = connection_services_challenge_button()

def create_statistics_button(parent_frame):

        def statistics_action():
            window_statistics_player = tk.Toplevel(parent_frame)
            window_statistics_player.title('Statistics for Players')
            window_statistics_player.geometry("410x500")
            window_statistics_player.resizable(False, False)
            window_statistics_player.configure(bg="#45a049")

            rank_title_label = tk.Label(window_statistics_player, text="Rank", bg="#45a049", fg="white",
                                        font=("Arial", 19))
            name_title_label = tk.Label(window_statistics_player, text="Name", bg="#45a049", fg="white",
                                        font=("Arial", 19))
            wins_title_label = tk.Label(window_statistics_player, text="Wins", bg="#45a049", fg="white",
                                        font=("Arial", 19))
            looses_title_label = tk.Label(window_statistics_player, text="Losses", bg="#45a049", fg="white",
                                          font=("Arial", 19))

            rank_title_label.grid(row=0, column=0)
            name_title_label.grid(row=0, column=1)
            wins_title_label.grid(row=0, column=2)
            looses_title_label.grid(row=0, column=3)

            try:
                show_statistics = player_service.show_statistics()

                for i, player_stats in enumerate(show_statistics):
                    tk.Label(window_statistics_player, text=player_stats["rank"], bg="#45a049", fg="white",
                             font=("Arial", 10)).grid(row=i + 1, column=0)
                    tk.Label(window_statistics_player, text=player_stats["name"], bg="#45a049", fg="white",
                             font=("Arial", 10)).grid(row=i + 1, column=1)
                    tk.Label(window_statistics_player, text=player_stats["wins"], bg="#45a049", fg="white",
                             font=("Arial", 10)).grid(row=i + 1, column=2)
                    tk.Label(window_statistics_player, text=player_stats["losses"], bg="#45a049", fg="white",
                             font=("Arial", 10)).grid(row=i + 1, column=3)

            except Exception as e:
                messagebox.showerror("Error in Statistics", f"Error: {e}")

        statistics_button = tk.Button(
            parent_frame,
            text="Statistics",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            height=2,
            bd=0,
            relief="solid",
            activebackground="#45a049",
            activeforeground="white",
            command=statistics_action,
        )
        return statistics_button