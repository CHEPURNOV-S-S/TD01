import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title("Крестики-нолики")
window.geometry("300x450")

current_player = "X"  # По умолчанию первый игрок - X
buttons = []
score_X = 0
score_O = 0
play_until_three_wins = tk.BooleanVar()  # Переменная для флажка

# Обновление счётчиков на экране
score_label = tk.Label(window, text=f"Счёт: X - {score_X}, O - {score_O}", font=("Arial", 14))
score_label.grid(row=4, column=0, columnspan=3, pady=10)

def update_score():
    global score_X, score_O
    score_label.config(text=f"Счёт: X - {score_X}, O - {score_O}")

def is_draw():
    for but_row in buttons:
        for cur_btn in but_row:
            if cur_btn["text"] == "":
                return False
    return True

def check_winner():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != "":
            return True
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != "":
            return True

    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != "":
        return True
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != "":
        return True

    return False

def reset_game(full_reset=False):
    global current_player
    global score_X, score_O
    if full_reset:
        choose_first_player()  # Выбор первого игрока перед началом новой игры
        score_X = 0
        score_O = 0
        update_score()

    for btn_row in buttons:
        for cur_btn in btn_row:
            cur_btn["text"] = ""  # Очищаем текст на всех кнопках

def check_end_of_game(winner):
    global score_X, score_O
    if play_until_three_wins.get():  # Если режим "до трёх побед" включён
        if winner == "X":
            score_X += 1
        elif winner == "O":
            score_O += 1
        update_score()

        if score_X == 3:
            messagebox.showinfo("Игра окончена", "Игрок X выиграл серию!")
            reset_series()
        elif score_O == 3:
            messagebox.showinfo("Игра окончена", "Игрок O выиграл серию!")
            reset_series()
    else:  # Если режим "до трёх побед" выключен
        if winner == "X":
            score_X += 1
        elif winner == "O":
            score_O += 1
        update_score()

def reset_series():
    global score_X, score_O
    score_X = 0
    score_O = 0
    update_score()
    reset_game(True)

def on_checkbox_change():
    if play_until_three_wins.get():  # Если флажок активирован
        print("Режим 'до трёх побед' включён")
    else:
        print("Режим 'до трёх побед' выключен")
    reset_game(True)  # Вызываем сброс игры

def choose_first_player():
    global current_player
    choice = messagebox.askquestion("Выбор первого игрока", "Кто будет ходить первым? (Да = X, Нет = O)")
    if choice == "yes":
        current_player = "X"
    else:
        current_player = "O"
    print(f"Первый ходит: {current_player}")

def on_click(row, col):
    global current_player

    if buttons[row][col]['text'] != "":
        return

    buttons[row][col]['text'] = current_player

    if check_winner():
        winner = current_player
        messagebox.showinfo("Игра окончена", f"Игрок {current_player} победил!")
        check_end_of_game(winner)
        reset_game()
    elif is_draw():
        messagebox.showinfo("Игра окончена", "Ничья!")
        reset_game()
    else:
        current_player = "O" if current_player == "X" else "X"

for i in range(3):
    row = []
    for j in range(3):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2, command=lambda r=i, c=j: on_click(r, c))
        btn.grid(row=i, column=j)
        row.append(btn)
    buttons.append(row)

# Кнопка перезапуска игры
reset_button = tk.Button(window, text="Перезапуск", font=("Arial", 14), command=lambda: reset_game(True))
reset_button.grid(row=3, column=0, columnspan=3, pady=10)

# Флажок для режима "до трёх побед"
three_wins_checkbox = tk.Checkbutton(window,
                                     text="Играть до трёх побед",
                                     variable=play_until_three_wins,
                                     command=on_checkbox_change)
three_wins_checkbox.grid(row=5, column=0, columnspan=3, pady=10)

# Выбор первого игрока перед началом игры
choose_first_player()

window.mainloop()