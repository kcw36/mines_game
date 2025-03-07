import random
from tkinter import (messagebox, Tk, DISABLED, NORMAL, Frame, Button, Entry, Label)

# randomly generate board with safe squares and bombs
def generate_board(num_bombs):
    num_safe = 25 - num_bombs
    squares = ['Safe'] * num_safe + ['Bomb'] * num_bombs
    random.shuffle(squares)
    return squares

# reveal whether the squares in the grid are safe or bombs
def reveal_board():
    for i in range(25):
        if board[i] == 'Bomb':
            buttons[i].config(text='💣', disabledforeground="red", state=DISABLED)
        else:
            buttons[i].config(text='✔', disabledforeground="green", state=DISABLED)

# calculate success probability of user bet and updates bet multiplier label as a response
def calculate_multiplier():
    global bet_multiplier

    try:
        num_bombs = int(entry_bombs.get())
        if num_bombs < 0 or num_bombs >= 25:
            raise ValueError
    except ValueError:
        multiplier_label.config(text="Payout Multiplier: -")
        return
    
    success_probability = 1.0
    remaining_safe = 25 - num_bombs
    remaining_total = 25
    
    for _ in range(len(chosen_squares)):
        success_probability *= remaining_safe / remaining_total
        remaining_safe -= 1
        remaining_total -= 1
    
    if len(chosen_squares) > 0:
        bet_multiplier = (1 / success_probability) * 0.94 
        update_multiplier_label()
    else:
        multiplier_label.config(text="Payout Multiplier: 1.00x")
    
    update_potential_returns()

# update potential returns based on bet amount and picks
def update_potential_returns():
    global bet_amount
    try:
        num_bombs = int(entry_bombs.get())
        bet_amount = float(entry_bet.get())
        if num_bombs < 0 or num_bombs >= 25:
            raise ValueError
    except ValueError:
        return
    
    pick_range = []
    if num_bombs <= 10:
        pick_range = [1, 2, 5, 10, 15]
    elif num_bombs <= 20:
        pick_range = range(1, 6)
    else:
        pick_range = [1]

    returns_text = "Potential Returns:\n"
    for picks in pick_range:
        success_probability = 1.0
        remaining_safe = 25 - num_bombs
        remaining_total = 25
        
        for _ in range(picks):
            success_probability *= remaining_safe / remaining_total
            remaining_safe -= 1
            remaining_total -= 1
        
        multiplier = (1 / success_probability) * 0.94
        returns_text += f"{picks} picks: £{(bet_amount * multiplier):.2f}\n"
    
    potential_returns_label.config(text=returns_text)

# behavior for when the square is selected by the user
def on_square_click(index):
    global safe_count, balance, bet_amount

    if 'chosen_squares' not in globals():
        messagebox.showinfo("Game Not Started.", "Please click the start game button before playing")
        return
    
    if index in chosen_squares:
        return

    chosen_squares.add(index)
    
    if board[index] == 'Bomb':
        buttons[index].config(text='💣', bg='red')
        messagebox.showinfo("Game Over", "BOOM! You hit a bomb!")
        reveal_board()
        balance -= bet_amount
        multiplier_label.config(text=f"Payout Multiplier: 1.00x") 
        payout_label.config(text=f"Current Return: -")
    else:
        buttons[index].config(text='✔', bg='green')
        calculate_multiplier()

    update_balance_label()
    update_return_label()

# gather user inputs from the interface and generates game board from result
def start_game():
    global board, chosen_squares, safe_count, bet_amount, num_bombs, bet_multiplier
    
    try:
        num_bombs = int(entry_bombs.get())
        bet_amount = float(entry_bet.get())

        if num_bombs < 0 or num_bombs >= 25:
            raise ValueError
        if bet_amount <= 0 or bet_amount > balance:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Setting defaults: 5 picks, 5 bombs, $10 bet.")
        num_bombs = 5
        bet_amount = 10

    board = generate_board(num_bombs)
    chosen_squares = set()
    safe_count = 0
    bet_multiplier = 1.0
    
    for i in range(25):
        buttons[i].config(text='?', bg='lightgray', state=NORMAL)

# allows user to close bet
def take_payout():
    global balance, bet_multiplier
    
    try:
        current_multiplier = bet_multiplier
        winnings = bet_amount * current_multiplier
        messagebox.showinfo("Payout Taken", f"You cashed out £{winnings:.2f}!")
        balance += winnings
    except ValueError:
        messagebox.showerror("Error", "Invalid multiplier value.")
        return
    except NameError:
        messagebox.showerror("Error", "Game not started")
        return
    
    update_balance_label()
    reveal_board()

# update return label based on new multiplier and bet amount
def update_return_label():
    payout_label.config(text=f"Current Return: ${bet_multiplier*bet_amount:.2f}")

# update multiplier label based on new multiplier
def update_multiplier_label():
    multiplier_label.config(text=f"Payout Multiplier: {bet_multiplier:.2f}x")

# update balance label based on new balance
def update_balance_label():
    balance_label.config(text=f"Balance: ${balance:.2f}")

# create user form
def create_form():
    global entry_bombs, entry_bet, balance_label, multiplier_label, payout_label, potential_returns_label

    label_bombs = Label(root, text="Enter the number of bombs:")
    label_bombs.pack()
    entry_bombs = Entry(root)
    entry_bombs.pack()
    entry_bombs.insert(0, "5")
    entry_bombs.bind("<KeyRelease>", lambda event: update_potential_returns())
    
    label_bet = Label(root, text="Enter your bet amount:")
    label_bet.pack()
    entry_bet = Entry(root)
    entry_bet.pack()
    entry_bet.insert(0, "10")
    entry_bet.bind("<KeyRelease>", lambda event: update_potential_returns())
    
    balance_label = Label(root, text=f"Balance: ${balance:.2f}")
    balance_label.pack()
    
    multiplier_label = Label(root, text="Payout Multiplier: 1.00x")
    multiplier_label.pack()

    payout_label = Label(root, text="Current Return: -")
    payout_label.pack()
    
    potential_returns_label = Label(root, text="Potential Returns:\n")
    potential_returns_label.pack()

# create buttons for form
def create_buttons():
    global buttons
    
    buttons = []
    for i in range(25):
        btn = Button(frame, text='?', width=4, height=2, command=lambda i=i: on_square_click(i))
        btn.grid(row=i // 5, column=i % 5)
        buttons.append(btn)
    
    start_button = Button(root, text="Start Game", command=start_game)
    start_button.pack()
    
    payout_button = Button(root, text="Take Payout", command=take_payout)
    payout_button.pack()

if __name__ == "__main__":
    root = Tk()
    root.title("Mines")
    
    balance = 100
    
    frame = Frame(root)
    frame.pack()
    
    create_form()
    create_buttons()
    
    root.mainloop()
