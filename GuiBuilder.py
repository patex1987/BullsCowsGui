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
        '''
        the __init__ method initializes the GUI, places all widgets on the
        interface
        '''
        master.wm_title("Bulls and Cows")
        self._load_images()
        self.master = master

        cur_row = 0
        cur_column = 0

        self.round_label = tk.Label(master, text='Round: 1')
        self.round_label.grid(row=cur_row, column=cur_column, columnspan=5,
                              sticky='ew')
        cur_row += 1

        vcmd = (master.register(self.onValidate), '%P', '%S')
        self.player_tip = tk.Entry(master,
                                   validate='key',
                                   justify='center',
                                   validatecommand=vcmd)
        self.player_tip.grid(row=cur_row, columnspan=6, sticky='ew')
        cur_row += 1

        self.submit_button = tk.Button(master, text='Submit')
        self.submit_button.columnconfigure(cur_row, weight=0)
        self.submit_button.grid(row=cur_row, columnspan=6, sticky='ew')
        cur_row += 1

        self.player_label = tk.Label(master, text='You')
        self.player_label.grid(row=cur_row, column=cur_column, columnspan=2,
                               sticky='ew')
        cur_column = 3
        self.computer_label = tk.Label(master, text='Computer')
        self.computer_label.grid(row=cur_row, column=cur_column, columnspan=2,
                                 sticky='ew')
        cur_column = 0
        cur_row += 1

        self.frames = []
        for i in range(5):
            frame = tk.Frame(master, width=60, height=1)
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

        self.game_result = tk.Label(master, text='')
        self.game_result.grid(row=cur_row, column=cur_column, columnspan=5)
        cur_column = 0
        cur_row += 1

        self.new_game_button = tk.Button(master, text='New Game')
        self.new_game_button.grid(row=cur_row, column=cur_column, columnspan=5,
                                  sticky='ew')

    def _load_images(self):
        '''
        loads resources (e.g. icons)
        '''
        self.bull_icon = tk.PhotoImage(file=r'.\img\Cultures-Bull-icon.png')
        self.cow_icon = tk.PhotoImage(file=r'.\img\Cow-icon.png')

    def onValidate(self, P, S):
        '''
        Only digits can be entered and the string cant
        be longer than 4 digits
        '''
        if S.isdigit() and len(P) < 5:
            return True
        else:
            self.master.bell()
            return False

    def update_bulls_cows(self, player_counts, computer_counts):
        '''
        Updates the count labels according to the actual round
        '''
        self.player_bull_count.config(text=str(player_counts[0]))
        self.player_cow_count.config(text=(player_counts[1]))
        self.computer_bull_count.config(text=(computer_counts[0]))
        self.computer_cow_count.config(text=(computer_counts[1]))

    def update_round(self, round_number):
        '''
        Updates the round counter
        '''
        self.round_label.config(text='Round: {0}'.format(round_number))

    def reset_gui(self):
        '''
        Resets the gui
        '''
        self.update_round(1)
        self.update_bulls_cows((0, 0), (0, 0))
        self.game_result.config(text='')
        self.player_tip.delete(0, 'end')

if __name__ == '__main__':
    ROOT = tk.Tk()
    GUI = BullsGui(ROOT)
    ROOT.resizable(width=False, height=False)
    ROOT.mainloop()
