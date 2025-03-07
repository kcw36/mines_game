import random
from tkinter import ( messagebox, Tk, DISABLED, NORMAL, Frame, Button, Entry, Label )

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

# behavior for when the square is selected by the user
def on_square_click(index):
    global safe_count, max_choices

    # check for chosen_squares variable to be made if not informs the user to trigger its creation
    if 'chosen_squares' not in globals():
        messagebox.showinfo("Game Not Started.", "Please click the start game button before playing")
        return
    
    # if the square has been selected before nothing happens
    if index in chosen_squares:
        return

    # adds the current square to the array of all selected squares
    chosen_squares.add(index)
    
    # when the square is a bomb ends the game and reveals board
    if board[index] == 'Bomb':
        buttons[index].config(text='💣', bg='red')
        messagebox.showinfo("Game Over", "BOOM! You hit a bomb!")
        reveal_board()
    # when the square is safe checks if the max number of guesses is reached if so user wins game if not continues to next guess
    else:
        buttons[index].config(text='✔', bg='green')
        safe_count += 1
        if safe_count == max_choices:
            messagebox.showinfo("You Win!", "Congratulations! You successfully picked all safe squares!")
            reveal_board()

# gather user inputs from the interface and generates game board from result
def start_game():
    global board, chosen_squares, safe_count, max_choices
    
    try:
        max_choices = int(entry_choices.get())
        num_bombs = int(entry_bombs.get())

        if max_choices <= 0 or max_choices > 25:
            raise ValueError
        if num_bombs < 0 or num_bombs >= 25:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Setting defaults: 5 picks, 5 bombs.")
        max_choices = 5
        num_bombs = 5
    
    board = generate_board(num_bombs)
    chosen_squares = set()
    safe_count = 0
    
    for i in range(25):
        buttons[i].config(text='?', bg='lightgray', state=NORMAL)

if __name__ == "__main__":
    # creates interface
    root = Tk()
    root.title("Mines")

    frame = Frame(root)
    frame.pack()

    # populates buttons in the grid for game
    buttons = []
    for i in range(25):
        btn = Button(frame, text='?', width=4, height=2, command=lambda i=i: on_square_click(i))
        btn.grid(row=i // 5, column=i % 5)
        buttons.append(btn)

    # creates entry forms for user
    label_choices = Label(root, text="Enter the number of squares to pick:")
    label_choices.pack()

    entry_choices = Entry(root)
    entry_choices.pack()
    entry_choices.insert(0, "5")

    label_bombs = Label(root, text="Enter the number of bombs:")
    label_bombs.pack()

    entry_bombs = Entry(root)
    entry_bombs.pack()
    entry_bombs.insert(0, "5")

    # creates start game button
    start_button = Button(root, text="Start Game", command=start_game)
    start_button.pack()

    # runs the game
    root.mainloop()
