import tkinter as tk
from tkinter import messagebox, Toplevel
import random

# ------- Dark Blue Theme ------- #
TEXT_COLOR = "#ffffff"
BG_COLOR = "#0a0f24"        # Dark navy blue
BUTTON_BG = "#1c2b4a"
TEXT_BOX_BG = "#0d1117"
TEXT_BOX_FG = "#ffffff"

# Fonts
FONT_TITLE = ("Helvetica", 20)
FONT_TEXT = ("Courier New", 12)
FONT_BUTTON = ("Verdana", 11 )

# ------- Data Classes ------- #
class Team:
    def __init__(self, name, members, rank):
        self.name = name
        self.members = members
        self.rank = rank

class Match:
    def __init__(self, team1, team2, round_name):
        self.team1 = team1
        self.team2 = team2
        self.round_name = round_name
        self.status = "Scheduled"
        self.winner = None

    def complete(self):
        self.status = "Completed"
        self.winner = random.choice([self.team1, self.team2])

class Scheduler:
    def __init__(self):
        self.teams = []
        self.group_A = []
        self.group_B = []
        self.rounds = {
            "Round 1": [],
            "Quarter Final": [],
            "Semi Final": [],
            "Final": []
        }

    def load_teams(self, filename):
        self.teams = []
        with open(filename, 'r') as file:
            for line in file:
                name, members, rank = line.strip().split(";")
                team = Team(name, members.split(","), int(rank))
                self.teams.append(team)
        self.teams.sort(key=lambda t: t.rank)

    def divide_groups(self):
        self.group_A = self.teams[:8]
        self.group_B = self.teams[8:]

    def schedule_matches(self, teams, round_name):
        random.shuffle(teams)
        matches = []
        for i in range(0, len(teams), 2):
            match = Match(teams[i], teams[i + 1], round_name)
            matches.append(match)
        self.rounds[round_name] = matches
        return matches

    def complete_round(self, round_name):
        for match in self.rounds[round_name]:
            match.complete()
        return [m.winner for m in self.rounds[round_name]]

# ------- GUI Application ------- #
class TournamentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cybersecurity Hackathon Scheduler")
        self.root.geometry("900x650")
        self.root.config(bg=BG_COLOR)

        self.scheduler = Scheduler()

        self.show_load_window()

    def clear_window(self, window):
        for widget in window.winfo_children():
            widget.destroy()

    def show_load_window(self):
        self.clear_window(self.root)

        title = tk.Label(self.root, text="Cybersecurity Hackathon Scheduler",
                         font=FONT_TITLE, fg=TEXT_COLOR, bg=BG_COLOR)
        title.pack(pady=20)

        btn_load = tk.Button(self.root, text="Load Teams", font=FONT_BUTTON,
                             bg=BUTTON_BG, fg=TEXT_COLOR,
                             command=self.load_teams)
        btn_load.pack(pady=100)

    def load_teams(self):
        try:
            self.scheduler.load_teams("teams.txt")
            messagebox.showinfo("Success", "Teams loaded successfully!")
            self.show_group_window()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_group_window(self):
        self.clear_window(self.root)

        tk.Label(self.root, text="Team Groups", font=FONT_TITLE, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

        text_area = tk.Text(self.root, height=20, width=90, bg=TEXT_BOX_BG,
                            fg=TEXT_BOX_FG, font=FONT_TEXT, wrap=tk.WORD)
        text_area.pack(pady=20)

        def divide():
            self.scheduler.divide_groups()
            text_area.insert(tk.END, "=== Group A (Top 8) ===\n")
            for t in self.scheduler.group_A:
                text_area.insert(tk.END, f"{t.rank}. {t.name}\n")
            text_area.insert(tk.END, "\n=== Group B (Bottom 8) ===\n")
            for t in self.scheduler.group_B:
                text_area.insert(tk.END, f"{t.rank}. {t.name}\n")

        btn_divide = tk.Button(self.root, text="Divide Groups", font=FONT_BUTTON,
                               bg=BUTTON_BG, fg=TEXT_COLOR, command=divide)
        btn_divide.pack(pady=5)

        btn_next = tk.Button(self.root, text="Next (Round 1)", font=FONT_BUTTON,
                             bg=BUTTON_BG, fg=TEXT_COLOR, command=self.show_round1_window)
        btn_next.pack(pady=5)

    def show_round1_window(self):
        self.show_round_window("Round 1")

    def show_round_window(self, round_name):
        self.clear_window(self.root)

        tk.Label(self.root, text=round_name, font=FONT_TITLE, fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=10)

        text_area = tk.Text(self.root, height=20, width=90, bg=TEXT_BOX_BG,
                            fg=TEXT_BOX_FG, font=FONT_TEXT, wrap=tk.WORD)
        text_area.pack(pady=20)

        def run_round():
            text_area.insert(tk.END, f"\n--- {round_name} ---\n")
            if round_name == "Round 1":
                a = self.scheduler.group_A[:]
                b = self.scheduler.group_B[:]
                random.shuffle(a)
                random.shuffle(b)
                teams = []
                for t1, t2 in zip(a, b):
                    teams.extend([t1, t2])
            else:
                prev = {
                    "Quarter Final": "Round 1",
                    "Semi Final": "Quarter Final",
                    "Final": "Semi Final"
                }[round_name]
                teams = [m.winner for m in self.scheduler.rounds[prev]]

            self.scheduler.schedule_matches(teams, round_name)
            self.scheduler.complete_round(round_name)

            for m in self.scheduler.rounds[round_name]:
                text_area.insert(tk.END, f"{m.team1.name} vs {m.team2.name} --> Winner: {m.winner.name}\n")

        tk.Button(self.root, text=f"Run {round_name}", font=FONT_BUTTON,
                  bg=BUTTON_BG, fg=TEXT_COLOR, command=run_round).pack(pady=5)

        if round_name != "Final":
            next_round = {
                "Round 1": "Quarter Final",
                "Quarter Final": "Semi Final",
                "Semi Final": "Final"
            }[round_name]
            tk.Button(self.root, text=f"Next ({next_round})", font=FONT_BUTTON,
                      bg=BUTTON_BG, fg=TEXT_COLOR, command=lambda: self.show_round_window(next_round)).pack(pady=5)
        else:
            tk.Button(self.root, text="Show Winner", font=FONT_BUTTON,
                      bg=BUTTON_BG, fg=TEXT_COLOR, command=self.show_winner_window).pack(pady=5)

    def show_winner_window(self):
        self.clear_window(self.root)

        if not self.scheduler.rounds["Final"]:
            teams = [m.winner for m in self.scheduler.rounds["Semi Final"]]
            self.scheduler.schedule_matches(teams, "Final")
            self.scheduler.complete_round("Final")

        winner = self.scheduler.rounds["Final"][0].winner

        tk.Label(self.root, text="🏆 Tournament Winner 🏆", font=FONT_TITLE,
                 fg=TEXT_COLOR, bg=BG_COLOR).pack(pady=50)

        tk.Label(self.root, text=winner.name, font=("Helvetica", 22, "bold"),
                 fg="#FFD700", bg=BG_COLOR).pack(pady=20)

# ------- Run App ------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentGUI(root)
    root.mainloop()
