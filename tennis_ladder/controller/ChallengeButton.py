import tkinter as tk
from tkinter import messagebox

from db_utils.DBUtils import DBUtils

from service.PlayerService import PlayerService
from service.MatchService import MatchService
from repository.PlayerRepository import PlayerRepository
from repository.MatchRepository import  MatchRepository
from repository.LeagueRoundRepository import LeagueRoundRepository
from DBInit import DBInit

def connection_services_challenge_button():
    db_utils = DBUtils()
    db_init = DBInit()
    session = db_init.session
    player_repository = PlayerRepository(session)
    match_repository = MatchRepository(session)
    league_round_repository = LeagueRoundRepository(session)
    player_service = PlayerService(session, player_repository)
    match_service = MatchService(session, match_repository, player_repository, league_round_repository)
    return player_service, db_utils, db_init, session, match_repository, player_repository, league_round_repository, match_service

def create_challenge_button(parent_frame, refresh_leaderboard):

    def challenge_action():
        new_window_for_challenge = tk.Toplevel(parent_frame)
        new_window_for_challenge.title('Challenge for Players')
        new_window_for_challenge.geometry("810x200")
        new_window_for_challenge.resizable(True, True)

        player_service, db_utils, db_init, session, match_repository, player_repository, league_round_repository, match_service = connection_services_challenge_button()

        player_service_initialization = player_service
        show_players_for_option_menu = player_service_initialization.get_all_players()
        list_of_players = [each_player.name for each_player in show_players_for_option_menu]

        #Δημιουργια Frame.
        frame_menu = tk.Frame(new_window_for_challenge,bg="#45a049",height='100',width='200',bd='3',relief="sunken")
        frame_menu.pack(anchor='center')
        value_for_option_menu_1 = tk.StringVar(new_window_for_challenge)
        value_for_option_menu_2 = tk.StringVar(new_window_for_challenge)
        value_for_option_menu_1.set("Select Player 1")
        value_for_option_menu_2.set("Select Player 2")

        option_menu_challenge_1 = tk.OptionMenu(frame_menu, value_for_option_menu_1, *list_of_players)
        option_menu_challenge_1.grid(row=0, column=1, padx='10', pady='10')
        player_1_label = tk.Label(frame_menu, text="Player 1",bg="#45a049", fg="white" ,font=("Arial", 12))
        player_1_label.grid(row=0, column=0, padx='10', pady='10')

        option_menu_challenge_2 = tk.OptionMenu(frame_menu, value_for_option_menu_2, *list_of_players)
        option_menu_challenge_2.grid(row=1, column=1, padx='10', pady='10')
        player_2_label = tk.Label(frame_menu, text="Player 2",bg="#45a049", fg="white",font=("Arial", 12))
        player_2_label.grid(row=1, column=0, padx='10', pady='10')

        show_player_name_1_label = tk.Label(frame_menu, text='',bg="#45a049", fg="white",font=("Arial", 12))
        show_player_name_1_label.grid(row=2, column=0)
        show_player_name_2_label = tk.Label(frame_menu, text='',bg="#45a049", fg="white",font=("Arial", 12))
        show_player_name_2_label.grid(row=2, column=2)

        select_button_option_menu_1 = tk.Button(frame_menu, text='Select',
                                                command=lambda: show_player_name_1_label.config(
                                                    text=f"Player 1 Selection: {value_for_option_menu_1.get()}"),bg="#45a049", fg="white",font=("Arial", 12))
        select_button_option_menu_1.grid(row=0, column=3, padx='10', pady='10')

        select_button_option_menu_2 = tk.Button(frame_menu, text='Select',
                                                command=lambda: show_player_name_2_label.config(
                                                    text=f"Player 2 Selection: {value_for_option_menu_2.get()}"),bg="#45a049", fg="white",font=("Arial", 12))
        select_button_option_menu_2.grid(row=1, column=3, padx='10', pady='10')

        def start_challenge():
            global name_of_challenger, name_of_opponent, match_result
            name_of_challenger = value_for_option_menu_1.get()
            name_of_opponent = value_for_option_menu_2.get()

            if name_of_challenger == "Select Player 1" or name_of_opponent == "Select Player 2":
                messagebox.showwarning("Invalid Selection", "Please select both players before proceeding.")
                new_window_for_challenge.destroy()
                return
            if name_of_challenger == name_of_opponent:
                messagebox.showwarning("Invalid Selection", "Player 1 and Player 2 cannot be the same.")
                new_window_for_challenge.destroy()
                return

            try:
                global all_players_list, id_of_challenger, id_of_opponent
                all_players_list = player_service_initialization.get_all_players()

                if len(all_players_list) % 2 != 0:
                    messagebox.showwarning(
                        "Invalid Player Count",
                        "Cannot simulate a round: the number of players must be even."
                    )
                    new_window_for_challenge.destroy()
                    return

                id_of_challenger = ''
                id_of_opponent = ''
                for index in all_players_list:
                    if index.name == name_of_challenger:
                        id_of_challenger = index.player_id
                    elif index.name == name_of_opponent:
                        id_of_opponent = index.player_id

                match_result = match_service.simulate_round(id_of_challenger, id_of_opponent)

                if not match_result or (isinstance(match_result, dict) and "error" in match_result):
                    error_msg = match_result.get("error", "Could not create match.")
                    messagebox.showerror("Invalid Match", error_msg)
                    new_window_for_challenge.destroy()
                    return

                if isinstance(match_result, dict) and "tournament_winner" in match_result:
                    messagebox.showinfo("🏆 Tournament Complete",
                                        f"The tournament has ended!\nWinner: {match_result['tournament_winner']}")
                else:
                    summary = ""
                    for result in match_result:
                        summary += f"{result['challenger']} vs {result['opponent']} → Winner: {result['winner']} ({result['score']})\n"
                    messagebox.showinfo("Round Completed", summary)

                messagebox.showinfo("Success", "The challenge has been simulated successfully.")
                refresh_leaderboard()
                new_window_for_challenge.destroy()

            except Exception as e:
                messagebox.showerror("Error", str(e))
                new_window_for_challenge.destroy()

        start_challenge_button = tk.Button(frame_menu, text='Start Challenge',font=("Arial", 12), command=start_challenge)
        start_challenge_button.grid(row=4, column=1, padx='10', pady='10')

    challenge_button = tk.Button(parent_frame, text="Challenge", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                 width=20, height=2, bd=0, relief="solid", activebackground="#45a049",
                                 activeforeground="white" ,command=challenge_action)
    return challenge_button