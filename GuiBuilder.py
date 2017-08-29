'''
Created on 27. 8. 2017

@author: patex1987
'''

import tkinter as tk


class BullsGui(object):
    '''
    Bulls and Cows GUI class
    '''
    def __init__(self, master):

        self.load_images()

        cur_row = 0
        cur_column = 0

        main_menu = tk.Menu(master)
        master.config(menu=main_menu)
        help_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='About', command=self.get_about)

        self.round_label = tk.Label(master, text='Round: 1')
        self.round_label.grid(row=cur_row, column=cur_column, columnspan=5, sticky='ew')
        cur_row += 1

        self.player_tip = tk.Entry(master, justify='center')
        self.player_tip.grid(row=cur_row, columnspan=6, sticky='ew')
        cur_row += 1

        self.submit_button = tk.Button(master, text='Submit')
        # master.columnconfigure(cur_row, weight=0)
        self.submit_button.columnconfigure(cur_row, weight=0)
        self.submit_button.grid(row=cur_row, columnspan=6, sticky='ew')
        cur_row += 1

        self.player_label = tk.Label(master, text='You')
        self.player_label.grid(row=cur_row, column=cur_column, columnspan=2, sticky='ew')
        cur_column = 3
        self.computer_label = tk.Label(master, text='Computer')
        self.computer_label.grid(row=cur_row, column=cur_column, columnspan=2, sticky='ew')
        cur_column = 0
        cur_row += 1

        self.frames = []
        for i in range(5):
            frame = tk.Frame(master, width=64, height=10)
            self.frames.append(frame)
            self.frames[i].grid(row=cur_row, column=i)

        cur_column = 0
        cur_row += 1

        self.player_bull_label = tk.Label(master, image=self.bull_icon)
        self.player_bull_label.grid(row=cur_row, column=cur_column)
        cur_column = 1
        self.player_cow_label = tk.Label(master, image=self.cow_icon)
        self.player_cow_label.grid(row=cur_row, column=cur_column)
        cur_column = 3
        self.computer_bull_label = tk.Label(master, image=self.bull_icon)
        self.computer_bull_label.grid(row=cur_row, column=cur_column)
        cur_column = 4
        self.computer_cow_label = tk.Label(master, image=self.cow_icon)
        self.computer_cow_label.grid(row=cur_row, column=cur_column)
        cur_column = 0
        cur_row += 1

        self.player_bull_count = tk.Label(master, text='0')
        self.player_bull_count.grid(row=cur_row, column=cur_column)
        cur_column = 1
        self.player_cow_count = tk.Label(master, text='0')
        self.player_cow_count.grid(row=cur_row, column=cur_column)
        cur_column = 3
        self.computer_bull_count = tk.Label(master, text='0')
        self.computer_bull_count.grid(row=cur_row, column=cur_column)
        cur_column = 4
        self.computer_cow_count = tk.Label(master, text='0')
        self.computer_cow_count.grid(row=cur_row, column=cur_column)
        cur_column = 0
        cur_row += 1

        self.game_result = tk.Label(master, text='End')
        self.game_result.grid(row=cur_row, column=cur_column, columnspan=5)
        cur_column = 0
        cur_row += 1

        self.new_game_button = tk.Button(master, text='New Game')
        self.new_game_button.grid(row=cur_row, column=cur_column, columnspan=5, sticky='ew')

    def get_about(self):
        '''
        Prints the about message
        '''
        return

    def load_images(self):
        '''
        loads resources
        '''
        self.bull_icon = tk.PhotoImage(file=r'.\img\Cultures-Bull-icon.png')
        self.cow_icon = tk.PhotoImage(file=r'.\img\Cow-icon.png')

root = tk.Tk()
gui = BullsGui(root)
root.mainloop()
