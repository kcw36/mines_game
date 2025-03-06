import random
from tkinter import ( messagebox, Tk, DISABLED, NORMAL, Frame, Button, Entry, Label )

def generate_board(num_bombs):
    num_safe = 25 - num_bombs
    squares = ['Safe'] * num_safe + ['Bomb'] * num_bombs
    random.shuffle(squares)
    return squares

def reveal_board():
    for i in range(25):
        if board[i] == 'Bomb':
            buttons[i].config(text='💣', disabledforeground="red", state=DISABLED)
        else:
            buttons[i].config(text='✔', disabledforeground="green", state=DISABLED)

def on_square_click(index):
    global safe_count, max_choices

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
    else:
        buttons[index].config(text='✔', bg='green')
        safe_count += 1
        if safe_count == max_choices:
            messagebox.showinfo("You Win!", "Congratulations! You successfully picked all safe squares!")
            reveal_board()

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
    root = Tk()
    root.title("Mines")
    root.geometry("200x320")

    frame = Frame(root)
    frame.pack()

    buttons = []
    for i in range(25):
        btn = Button(frame, text='?', width=4, height=2, command=lambda i=i: on_square_click(i))
        btn.grid(row=i // 5, column=i % 5)
        buttons.append(btn)

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

    start_button = Button(root, text="Start Game", command=start_game)
    start_button.pack()

    root.mainloop()
