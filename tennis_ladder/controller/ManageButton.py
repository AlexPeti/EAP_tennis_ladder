import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

from repository.LeagueRoundRepository import LeagueRoundRepository

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from service.PlayerService import PlayerService
from repository.PlayerRepository import PlayerRepository
from DBInit import DBInit


def ManageButton(parent_frame, refresh_leaderboard):
    """
    Create and return a Manage button for the Tennis Ladder application.
    :param parent_frame: The frame where the button will be placed.
    :param refresh_leaderboard: Function to refresh the leaderboard.
    :return: The Manage button instance.
    """
    # Initialize the database session and services
    db_init = DBInit()
    player_repository = PlayerRepository(db_init.session)
    player_service = PlayerService(db_init.session, player_repository)
    league_round_repository = LeagueRoundRepository(db_init.session)

    def manage_action():
        """
        Function to handle the Manage button action.
        Opens a new window for managing players.
        """

        # Check if any league round has started
        rounds_played = league_round_repository.get_total_rounds()
        if rounds_played > 0:
            messagebox.showwarning(
                "Action Not Allowed",
                "Player management is disabled once the tournament has started."
            )
            return

        manage_window = tk.Toplevel(parent_frame)
        manage_window.title("Manage Players")
        manage_window.geometry("400x300")

        # Frame for adding a player
        add_frame = tk.Frame(manage_window, bg="green")
        add_frame.pack(pady=10)

        tk.Label(add_frame, text="Add New Player:", font=("Arial", 12)).pack(anchor="w")
        add_player_entry = tk.Entry(add_frame, width=30)
        add_player_entry.pack(pady=5)

        def add_player():
            player_name = add_player_entry.get()
            if player_name:
                try:
                    player_service.add_player(player_name)
                    messagebox.showinfo("Success", f"Player '{player_name}' added successfully!")
                    add_player_entry.delete(0, tk.END)
                    refresh_leaderboard()  # Refresh the leaderboard
                    refresh_player_dropdown()  # Refresh the dropdown menu
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to add player: {e}")
                finally:
                    manage_window.lift()  # Bring the window to the front
            else:
                messagebox.showwarning("Input Error", "Please enter a player name.")
                manage_window.lift()  # Bring the window to the front

        tk.Button(add_frame, text="Add Player", command=add_player, bg="#4CAF50", fg="white").pack(pady=5)

        # Frame for deleting a player
        delete_frame = tk.Frame(manage_window, bg="red")
        delete_frame.pack(pady=10)

        tk.Label(delete_frame, text="Delete Player:", font=("Arial", 12)).pack(anchor="w")

        # Dropdown menu for selecting a player to delete
        player_dropdown = ttk.Combobox(delete_frame, width=30, state="readonly")
        player_dropdown.pack(pady=5)

        def refresh_player_dropdown():
            """
            Refresh the dropdown menu with the list of players.
            """
            try:
                players = player_repository.get_all()
                player_dropdown['values'] = [f"{player.player_id}: {player.name}" for player in players]
                if players:
                    player_dropdown.current(0)  # Select the first player by default
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load players: {e}")

        def delete_player():
            selected_player = player_dropdown.get()
            if selected_player:
                player_id = int(selected_player.split(":")[0])  # Extract player ID from the dropdown value
                try:
                    player_service.delete_player(player_id)
                    messagebox.showinfo("Success", f"Player with ID {player_id} deleted successfully!")
                    refresh_leaderboard()  # Refresh the leaderboard
                    refresh_player_dropdown()  # Refresh the dropdown menu
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete player: {e}")
                finally:
                    manage_window.lift()  # Bring the window to the front
            else:
                messagebox.showwarning("Input Error", "Please select a player to delete.")
                manage_window.lift()  # Bring the window to the front

        tk.Button(delete_frame, text="Delete Player", command=delete_player, bg="#f44336", fg="white").pack(pady=5)

        # Populate the dropdown menu initially
        refresh_player_dropdown()

    button = tk.Button(
        parent_frame,
        text="Manage",
        font=("Arial", 12, "bold"),
        bg="#4CAF50",
        fg="white",
        width=20,
        height=2,
        bd=0,
        relief="solid",
        activebackground="#45a049",
        activeforeground="white",
        command=manage_action,
    )
    return button