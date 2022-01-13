import tkinter as tk
import random
import colors as c


class Game(tk.Frame):
    def __init__(self):

        tk.Frame.__init__(self)

        # making a widget manager which splits master widget into rows and columns
        self.grid()

        # Setting Master Widget's Title
        self.master.title('2048')

        # Frame is managing/containing the cells(2D) inside itself, created by grid(). Actually this main_grid has all the cells which we are displacing.
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=400, height=400)

        # formatting the grid() padding it with repsect to y-axis
        self.main_grid.grid(pady=(80, 0))

        self.make_GUI()
        self.start_game()

        # .bind() associates shortcut keys to use them as input
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)

        self.mainloop()

    def make_GUI(self):
        #MAKING A MAIN WINDOW FRAME, MAKING 4*4 CELLS AND SETS SCORE TO ZERO
        # make a list in which cells will be stored
        self.cells = []

        for i in range(4):

            #creating a list "row"
            row = []
            for j in range(4):
                # .Frame() makes a container containing / managing widgets. Taking main_grid created first in __init__ , as argument
                cell_frame = tk.Frame(self.main_grid, bg=c.EMPTY_CELL_COLOR, width=100, height=100)

                #grid distributes the master widget into rows and columns
                cell_frame.grid(row=i, column=j, padx=5, pady=5)

                # .Label() creates a display box over widgets, it shows text/images. Update-able
                # here every cell of main_grid is being assigned by a cell number by using Label() function
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)

                #closing grid() statement
                cell_number.grid(row=i, column=j)

                # creating a dictionary, line responsible for accessing each frame by their cell_frame and each cell's number by cell_number
                cell_data = {"frame": cell_frame, "number": cell_number}

                # update each element of cell_data dictionary in list named "row"
                # row=[cell_data, cell_data, cell_data, cell_data]
                row.append(cell_data)
            #  cells=[[row],[row],[row],[row]] ; when we come out of loop we just finished creating a 2Dimensional list
            self.cells.append(row)

        # making SCORE header
        score_frame = tk.Frame(self)

        # setting the frame
        score_frame.place(relx=0.5, y=40, anchor="center")

        tk.Label(score_frame, text="Score",font=c.SCORE_LABEL_FONT).grid(row=0)

        #SETTING INITIAL SCORE TO ZERO
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)

        self.score_label.grid(row=1)

    def start_game(self):
        #shows tiles
        # create matrix of zeroes
        self.matrix = [[0] * 4 for _ in range(4)]  # row, column

        # fill 2 random cells with 2s
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        self.matrix[row][col] = 2

        # game has been started with first two tiles with 2's

        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text="2")

        # the reason why we are doing it again is that ONCE WE HAVE STARTED GAME, IT NEEDS TO PUT TILES DURING EVERY MOVE
        # while loop is searching for another non-zero tile
        while (self.matrix[row][col] != 0):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2], fg=c.CELL_NUMBER_COLORS[2], font=c.CELL_NUMBER_FONTS[2], text="2")
        #.configure() ;- configures resources of a widget.

        self.score = 0

    # Matrix Manipulation Functions

    def stack(self):
        # Stack ( [ 0 ] [ 0 ] [ 4 ] [ 2 ]  )
        # Stack ( [ 4 ] [ 0 ] [ 0 ] [ 2 ]  )
        #       ( [ 4 ] [ 2 ] [ 0 ] [ 0 ]  )

        # makes a copy of the original game board matrix and move tiles.
        new_matrix = [[0] * 4 for _ in range(4)]  #row, column
        for i in range(4):

            # fill_position is an iterator which iterates when a number is found in
            fill_position = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    new_matrix[i][fill_position] = self.matrix[i][j]
                    fill_position += 1
        self.matrix = new_matrix

    def combine(self):
        # combines two cells ( like [ 2 ] [ 2 ] --> [ 4 ] )
        # upadtes the score
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]

    def reverse(self):
        # This Method mirrors the matrix HORIZONTALLY
        # [ [ 0 , 0 , 0 ],                                      [ [ 0 , 0 , 0 ],
        #   [ 1 , 2 , 3 ],  -----> (reverse() func applied )      [ 3 , 2 , 1 ],
        #   [ 4 , 5 , 6 ] ]                                       [ 6 , 5 , 4 ] ]
        new_matrix = []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3 - j])
        self.matrix = new_matrix

    def transpose(self):
        # transposes the cells / matrix
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix = new_matrix

    # Add a new 2 or 4 tile randomly to an empty cell

    def add_new_tile(self):
        # this function first detects that whether there is an empty tile ( tile having value 0 ) in matrix
        # if found then place a tile at that position of num either 2 or 4

        # The any() function returns True if an item in an iterable is true, otherwise it returns False
        # row is a local variable
        if any(0 in row for row in self.matrix):
            row = random.randint(0, 3)
            col = random.randint(0, 3)
            while (self.matrix[row][col] != 0):
                row = random.randint(0, 3)
                col = random.randint(0, 3)

            # Return a random element from a list
            # adds tile having either 2 or 4
            self.matrix[row][col] = random.choice([2, 4])

    # Update the GUI to match the matrix

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]

                # if the cell_value has zero it means it is an empty tile, so we adding text=''
                if cell_value == 0:

                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)

                    self.cells[i][j]["number"].configure(
                        bg=c.EMPTY_CELL_COLOR, text="")

                else:

                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])

                    # if cell_value is non-zero, we convert it into string and set it as text of our tile
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value],
                                                         fg=c.CELL_NUMBER_COLORS[cell_value],
                                                         font=c.CELL_NUMBER_FONTS[cell_value],
                                                         text=str(cell_value))

        # updating score in GUI interface, score_label is used and updated in combine()
        self.score_label.configure(text=self.score)

        self.update_idletasks()
        '''update_idetasks() :- Enter event loop until all idle callbacks have been called. This
        will update the display of windows but not process events caused by
        the user. Taken from Documentation.'''


    # Check if any moves are possible

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):

                #consider that a board in which all tiles are filled, but there are two same numbers in a row [[2,2,..,..],[4,8,etc],...], 2 and 2 can be combined
                # so it is checking this condition if yes, it returns True
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False


    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):

                #consider that a board in which all tiles are filled, but there is [[2,...],[2,....],...], 2 and 2 can be combined
                # so it is checking this condition if yes, it returns True
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    # Check if Game is Over (Win/Lose)

    def game_over(self):

        # Game overs when either any tile has 2048 number, or there is no (same) number which can be combined

        # checking if there is any 2048 number in the self.matrix
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="You win!",
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()

            # we have to add not 0 condition because sometimes a 2 is surrounded by empty tiles ( 0's )
            # in which both horizontal and vertical move exists function will return False that there is no move exists but there will be empty tiles

        elif not any (0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5, anchor="center")
            tk.Label(
                game_over_frame,
                text="Game over!",
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()



    # Arrow-Press Functions

    def left(self, event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()



def main():
    Game()


if __name__ == "__main__":
    main()
