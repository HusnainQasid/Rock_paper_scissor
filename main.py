import sys
import random
from collections import Counter
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

# ================= GAME LOGIC =================
class RPSGame:
    def __init__(self):
        self.moves = ['rock', 'paper', 'scissors']
        self.history = []
        self.transition = {}

    def get_winner(self, user, ai):
        if user == ai:
            return "Draw"
        elif (user == "rock" and ai == "scissors") or \
             (user == "scissors" and ai == "paper") or \
             (user == "paper" and ai == "rock"):
            return "User Wins"
        else:
            return "AI Wins"

    def counter_move(self, move):
        return {"rock": "paper", "paper": "scissors", "scissors": "rock"}[move]

    def get_ans(self):
        if not self.history:
            return random.choice(self.moves)
        most_common = Counter(self.history).most_common(1)[0][0]
        return self.counter_move(most_common)

    def get_ans_trans(self):
        if len(self.history) < 1:
            return random.choice(self.moves)

        prev = self.history[-1]

        if prev in self.transition and self.transition[prev]:
            predicted = Counter(self.transition[prev]).most_common(1)[0][0]
            return self.counter_move(predicted)
        else:
            return self.get_ans()

    def update_transition(self):
        if len(self.history) < 2:
            return

        prev = self.history[-2]
        curr = self.history[-1]

        if prev not in self.transition:
            self.transition[prev] = []

        self.transition[prev].append(curr)

    def play(self, user_move, level):
        ai = self.get_ans() if level == 1 else self.get_ans_trans()

        self.history.append(user_move)
        self.update_transition()

        result = self.get_winner(user_move, ai)
        return ai, result


# ================= GUI =================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.game = RPSGame()
        self.level = 1
        self.user_score = 0
        self.ai_score = 0

        self.setWindowTitle("Rock Paper Scissors AI")
        self.setGeometry(300, 200, 400, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: white;
                font-family: Arial;
            }

            QPushButton {
                background-color: #3a3a5a;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #5a5aff;
            }

            QLabel {
                font-size: 16px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Title
        title = QLabel("Rock Paper Scissors")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        # Difficulty
        self.combo = QComboBox()
        self.combo.addItems(["Easy (Frequency)", "Medium (Markov)"])
        self.combo.currentIndexChanged.connect(self.change_level)
        layout.addWidget(self.combo)

        # Scoreboard
        self.score_label = QLabel("You: 0 | AI: 0")
        self.score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.score_label)

        # Result
        self.result_label = QLabel("Make your move!")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.result_label)

        # Buttons layout
        btn_layout = QHBoxLayout()

        rock_btn = QPushButton("🪨")
        paper_btn = QPushButton("📄")
        scissor_btn = QPushButton("✂️")

        rock_btn.clicked.connect(lambda: self.play("rock"))
        paper_btn.clicked.connect(lambda: self.play("paper"))
        scissor_btn.clicked.connect(lambda: self.play("scissors"))

        btn_layout.addWidget(rock_btn)
        btn_layout.addWidget(paper_btn)
        btn_layout.addWidget(scissor_btn)

        layout.addLayout(btn_layout)

        # Reset Button
        reset_btn = QPushButton("Reset Game")
        reset_btn.clicked.connect(self.reset_game)
        layout.addWidget(reset_btn)

        self.setLayout(layout)

    def change_level(self, index):
        self.level = index + 1

    def play(self, user_move):
        ai, result = self.game.play(user_move, self.level)

        # Update score
        if result == "User Wins":
            self.user_score += 1
            color = "#00ff88"
        elif result == "AI Wins":
            self.ai_score += 1
            color = "#ff4d4d"
        else:
            color = "#ffffff"

        self.score_label.setText(f"You: {self.user_score} | AI: {self.ai_score}")
        self.result_label.setStyleSheet(f"font-size: 18px; color: {color};")
        self.result_label.setText(f"You: {user_move}   AI: {ai}\n{result}")

    def reset_game(self):
        self.user_score = 0
        self.ai_score = 0
        self.game.history.clear()
        self.game.transition.clear()
        self.score_label.setText("You: 0 | AI: 0")
        self.result_label.setText("Game Reset!")


# ================= RUN =================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
