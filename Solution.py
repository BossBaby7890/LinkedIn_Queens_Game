import tkinter as tk
import random
from PIL import Image,ImageTk


class Queens_game():
    def __init__(self, board_size):
        self.board_size = board_size
        self.square_size = 40
        self.window = tk.Tk()
        self.Color = '#F5F5F5'
        self.board_color = {}
        self.queens_loc = []
        self.queen_img = ImageTk.PhotoImage(Image.open("queens_icon.png"))
        self.image_ids = []
        
    def create_board(self, canvas, size):
        board_size = size * self.square_size  
        offset_x = (440 - board_size) // 2  
        offset_y = (440 - board_size) // 2  

        for row in range(size):
            for col in range(size):
                x1 = offset_x + col * self.square_size
                y1 = offset_y + row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "#F5F5F5" 
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def  highlight_overlapping(self, event):
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        overlapping = canvas.find_overlapping(x, y, x+1, y+1)
        for item in overlapping:
            initial_color = canvas.itemcget(item, option = 'fill')
            canvas.itemconfigure(item, fill=self.Color)
            
            if initial_color != "#F5F5F5":
                self.board_color[initial_color].remove(item)
                if self.Color in self.board_color.keys():
                    self.board_color[self.Color].append(item)
                else:
                    self.board_color[self.Color] = [item]

    
            elif initial_color == "#F5F5F5":
                if self.Color in self.board_color.keys():
                    self.board_color[self.Color].append(item)
                else:
                    self.board_color[self.Color] = [item]


    def select_color(self, color):
        self.Color = color
        
    def convert_to_grid(self,number, grid_size):
        number -= 1  
        return number // grid_size, number % grid_size
    
    def same_row_column_diagonal(self,pos_1, pos_2):
        row_diff = abs(pos_1[0] - pos_2[0])
        col_diff = abs(pos_1[1] - pos_2[1])
        
        if row_diff == 0 or col_diff == 0:
            return True  
        
        if row_diff == 1 and col_diff == 1:
            return True
        
        return False 
            
    def solve(self, index):
        if index == len(self.board_color.keys()):  
            return True

        color = list(self.board_color.keys())[index]
        
        for pos in self.board_color[color]:
            pos_grid = self.convert_to_grid(pos, self.board_size)

            if all(not self.same_row_column_diagonal(self.convert_to_grid(q, self.board_size), pos_grid) for q in self.queens_loc):
                self.queens_loc.append(pos)  
                
                if self.solve(index + 1):  
                    return True

                self.queens_loc.pop()
        
        return False  # No valid position found for this color group
    
    def place_queens(self, canvas):
        if self.solve(0):
            print(f"Solution found: {self.queens_loc}")
            for loc in self.queens_loc:
                coords = canvas.coords(loc)
                mid_x = (coords[0] + coords[2])/2
                mid_y = (coords[1] + coords[3])/2
                img_id = canvas.create_image(mid_x, mid_y, anchor = tk.CENTER, image = self.queen_img)
                self.image_ids.append(img_id)
        else:
            print("No valid solution exists.")
    
    def reset(self, canvas):
        for id in self.image_ids:
            canvas.delete(id)
        
        self.image_ids.clear()
        self.queens_loc.clear()
        
    
    def main(self):
        self.window.geometry("650x550")
        self.window.maxsize(650,550)
        self.window.minsize(650,550)

        label = tk.Label(self.window, text="Queens Game Solver", 
                 font=("Helvetica", 18, "bold"),
                 fg="white",
                 bg="#4A90E2",
                 padx=20, pady=10,
                 borderwidth=3, relief="ridge",
                 width=25)

        label.pack(pady=10)

        canvas = tk.Canvas(self.window, width=440, height=440) 
        canvas.pack(side= tk.LEFT)

        self.create_board(canvas, self.board_size)
        canvas.bind("<Button-1>", self.highlight_overlapping)
        canvas.bind("<B1-Motion>", self.highlight_overlapping) 


        btn_frame = tk.Frame(self.window)
        btn_frame.pack(side=tk.LEFT)  

        top_btn_frame = tk.Frame(btn_frame)
        top_btn_frame.pack(side=tk.TOP, pady=10)

        reset_btn = tk.Button(master=top_btn_frame, background='gray', height=3, width=10, text='Reset',
                            command=lambda: self.reset(canvas=canvas), relief=tk.RAISED, border=5)
        reset_btn.grid(row=0, column=0, padx=5)

        solve_btn = tk.Button(master=top_btn_frame, background='gray', height=3, width=10, text='Solve',
                            command=lambda: self.place_queens(canvas=canvas), relief=tk.RAISED, border=5)
        solve_btn.grid(row=0, column=1, padx=5)

        color_grid_frame = tk.Frame(btn_frame)
        color_grid_frame.pack(side=tk.TOP, pady=10)

        color_bank = ['#96BEFF', '#FFC992', '#E6F388', '#DFDFDF', '#BBA3E2', '#B9B29E', 
                    '#FF7B60', '#B3DFA0', '#423f44', "#634963", "#223f44"]
        colors = random.sample(color_bank, k=self.board_size)

        clr_grid_size = 3

        for index, color in enumerate(colors):
            row, col = divmod(index, clr_grid_size)
            btn = tk.Button(color_grid_frame, background=color, height=2, width=5,
                            command=lambda c=color: self.select_color(c))
            btn.grid(row=row, column=col, padx=5, pady=5)
            
        self.window.mainloop()



game_1 = Queens_game(5)
game_1.main()