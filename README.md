
🏆 Cybersecurity Hackathon Scheduler
A Python-based GUI application that automates the scheduling of cybersecurity hackathon matches.
It divides teams into groups, creates matchups, and determines winners for each round (Round 1, Quarterfinals, Semifinals, and Final) in an interactive dark-themed Tkinter interface.

✨ Features
Automatic Team Management – Load teams from a teams.txt file.

Group Division – Splits teams into Group A (Top 8) and Group B (Bottom 8).

Round Scheduling – Schedules matches for Round 1, Quarterfinals, Semifinals, and Final.

Random Winner Generation – Automatically selects winners for each match.

Dark-Themed GUI – Minimalistic hacker-style dark blue interface.

Step-by-Step Windows – Each stage appears in a dedicated window for clarity.

📂 Project Structure
plaintext
Copy
Edit
hackathon_scheduler/
│
├── scheduler.py        # Main application file
├── teams.txt           # Team data file
├── screenshots/        # Contains GUI screenshots
│    ├── home.png
│    ├── groups.png
│    └── rounds.png
└── README.md           # Project documentation



🚀 How to Run
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/Ammarah-khalil/hackathon-scheduler.git
cd hackathon-scheduler
2. Add Team Data
Create a file teams.txt with this format:

python-repl
Copy
Edit
TeamA;Alice,Bob;1
TeamB;Charlie,David;2
TeamC;Eve,Frank;3
...
Format: TeamName;Member1,Member2;Rank

3. Run the Application
bash
Copy
Edit
python scheduler.py
🏆 Future Enhancements
Export match results to CSV or PDF.

Add manual winner selection feature.

Create a web-based version using Flask/Django.

👩‍💻 Author
Ammarah Khalil
Cybersecurity Enthusiast | Python Developer | SOC & Network Security
GitHub • LinkedIn
