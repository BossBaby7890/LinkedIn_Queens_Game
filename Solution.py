import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image,ImageTk
import time



class Queens_game():
    def __init__(self, board_size):
        self.board_size = board_size
        self.square_size = 40
        self.window = tk.Tk()
        self.sv = tk.StringVar()
        self.Color = '#EFDBDB'
        self.board_color = {}
        self.queens_loc = []
        self.queen_img = ImageTk.PhotoImage(Image.open("queens_icon.png"))
        self.image_ids = []
        self.visualize = False
        
    def create_board(self, canvas, size):
        board_size = size * self.square_size  
        canvas_width = int(canvas.cget("width"))  
        canvas_height = int(canvas.cget("height"))  

        offset_x = (canvas_width - board_size) // 2  
        offset_y = (canvas_height - board_size) // 2 

        for row in range(size):
            for col in range(size):
                x1 = offset_x + col * self.square_size
                y1 = offset_y + row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "#EFDBDB" 
                canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def  highlight_overlapping(self, event):
        if len(self.queens_loc) == self.board_size:
            tk.messagebox.showerror(message= "You cannot change the Color this Cell \nReset the board and Try again!")
        else:
            canvas = event.widget
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            overlapping = canvas.find_overlapping(x, y, x+1, y+1)
            for item in overlapping:
                initial_color = canvas.itemcget(item, option = 'fill')
                canvas.itemconfigure(item, fill=self.Color)
                
                if initial_color != "#EFDBDB":
                    self.board_color[initial_color].remove(item)
                    if self.Color in self.board_color.keys():
                        self.board_color[self.Color].append(item)
                    else:
                        self.board_color[self.Color] = [item]

        
                elif initial_color == "#EFDBDB":
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
                
    def solve(self, index, canvas):
        if index == len(self.board_color.keys()):
            return True

        color = list(self.board_color.keys())[index]
        
        for pos in self.board_color[color]:
            pos_grid = self.convert_to_grid(pos, self.board_size)

            if all(not self.same_row_column_diagonal(self.convert_to_grid(q, self.board_size), pos_grid) for q in self.queens_loc):
                self.queens_loc.append(pos)
                self.place_queen(canvas=canvas, loc=pos)
                if self.visualize:
                    self.window.update()
                    self.sv.set(self.queens_loc)
                    print(self.sv.get())
                    time.sleep(0.5)

    
                if self.solve(index + 1, canvas=canvas):  
                    return True

                self.queens_loc.pop()
                img_id = self.image_ids.pop()
                canvas.delete(img_id)
                if self.visualize:
                    self.window.update()
                    self.sv.set(self.queens_loc)
                    time.sleep(0.5)

        return False 
    
    def place_queen(self, canvas, loc):
        coords = canvas.coords(loc)
        mid_x = (coords[0] + coords[2])/2
        mid_y = (coords[1] + coords[3])/2
        img_id = canvas.create_image(mid_x, mid_y, anchor = tk.CENTER, image = self.queen_img)
        self.image_ids.append(img_id)

    def reset(self, canvas):
        if len(self.queens_loc) == self.board_size:
            for id in self.image_ids:
                canvas.delete(id)
            self.image_ids.clear()
            self.queens_loc.clear()
            self.sv.set("")
        else:
            tk.messagebox.showerror(message= "You cannot Reset at this Time\nWait for solution to finsh and try again!")
        

    def toggle(self, button: tk.Button):
        if button.config('relief')[-1] == 'sunken':
            self.visualize = False
            button.config(relief="raised", text='Instant')
        else:
            self.visualize = True
            button.config(relief="sunken", text='Visual')

    
    def main(self):
        self.window.title("Queens Game")
        self.window.geometry("685x550")
        self.window.maxsize(685,550)
        self.window.minsize(685,550)
        self.window.configure(bg='#FFB200')

        label = tk.Label(self.window, text="Queens Game Solver", 
                 font=("fixedsys", 23, 'bold'),
                 fg="#D91656", bg = "#FFB200")

        label.pack(pady=10)

        canvas = tk.Canvas(self.window, width=440, height=440, background="#EB5B00",highlightbackground="#640D5F",borderwidth=2, relief='solid') 
        canvas.pack(side= tk.LEFT, padx=4)

        self.create_board(canvas, self.board_size)
        canvas.bind("<Button-1>", self.highlight_overlapping)
        canvas.bind("<B1-Motion>", self.highlight_overlapping) 

        toggle_frame = tk.Frame(self.window, borderwidth=2, relief='solid', highlightbackground="#640D5F", background="#EB5B00")
        toggle_frame.pack(side = tk.TOP, pady= 20)
        
        toggleButton = tk.Button(master= toggle_frame, text="Instant", width=10, relief="raised", 
                                 command =lambda:self.toggle(toggleButton), background='#640D5F', foreground='white',font=("fixedsys"), border=5)
        toggleButton.pack(pady= 5)

        posLabel = tk.Label(master= toggle_frame, textvariable=self.sv, width=15, height=4, borderwidth=1, 
                            relief='solid', background="#D91656", foreground='white', font=("fixedsys", 4), wraplength=120)
        posLabel.pack()

        btn_frame = tk.Frame(self.window, background="#EB5B00", borderwidth=2, relief='solid', highlightbackground="#640D5F")
        btn_frame.pack(side=tk.LEFT, padx=3)  

        top_btn_frame = tk.Frame(btn_frame, background="#EB5B00")
        top_btn_frame.pack(side=tk.TOP, pady=10)

        reset_btn = tk.Button(master=top_btn_frame, background='#D91656', height=3, width=10, text='Reset',foreground='white',
                             font=("fixedsys"), command=lambda: self.reset(canvas=canvas), relief=tk.RAISED, border=5)
        reset_btn.grid(row=0, column=0, padx=5)

        solve_btn = tk.Button(master=top_btn_frame, background='#640D5F', height=3, width=10, text='Solve',foreground='white',
                            font=("fixedsys"), command=lambda: self.solve(index=0,canvas=canvas), relief=tk.RAISED, border=5)
        solve_btn.grid(row=0, column=1, padx=5)

        color_grid_frame = tk.Frame(btn_frame, background="#D2A24C")
        color_grid_frame.pack(side=tk.TOP, pady=10)

        color_bank = ['#96BEFF', '#FFC992', '#E6F388', '#BBBBBB', '#BBA3E2', '#B9B29E', 
                    '#FF7B60', '#B3DFA0', '#423f44', "#634963", "#223f44"]
        colors = random.sample(color_bank, k=self.board_size)

        clr_grid_size = 3

        for index, color in enumerate(colors):
            row, col = divmod(index, clr_grid_size)
            btn = tk.Button(color_grid_frame, background=color, height=2, width=5,
                            command=lambda c=color: self.select_color(c))
            btn.grid(row=row, column=col, padx=5, pady=5)
            
        self.window.mainloop()
