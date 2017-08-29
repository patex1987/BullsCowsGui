'''
Created on 29. 8. 2017

@author: patex1987
'''

import GuiBuilder
import BullsCowsComputerLogic as computer
import tkinter as tk
from tkinter import messagebox
from enum import Enum
import random


class GameState(object):
    '''
    class holding all game variables
    '''
    def __init__(self):
        self.round = 1
        self.possible_states = Enum('State', 'START INPROGRESS OVER')
        self.current_state = self.possible_states.START
        self.secret_number = self._generate_secret_number()
        self.computer_solution = None

    def _generate_secret_number(self):
        '''
        generates a new secret number to be guessed
        '''
        return "".join([str(x) for x in random.sample(range(10), 4)])

    def update_secret_number(self):
        '''
        generates new secret number at the beginning of new round
        '''
        self.secret_number = self._generate_secret_number()


def main_game():
    '''
    Handles the main loop of the game
    '''
    state = GameState()
    GUI.submit_button.bind('<Button-1>',
                           lambda event, game_state=state:
                           submit_guess(event, state))
    GUI.new_game_button.bind('<Button-1>',
                             lambda event, game_state=state:
                             start_new_game(event, state))
    state.computer_solution = computer.ComputerGuessAlgorithm1(state.secret_number,
                                                               '0123')
    return


def submit_guess(event, game_state):
    '''
    Checks the correctness of the user guess
    '''
    if game_state.current_state == game_state.possible_states.OVER:
        ROOT.bell()
        return
    print(game_state.current_state)
    guess = GUI.player_tip.get()
    if len(guess) != 4:
        ROOT.bell()
        return
    if len(set(guess)) != 4:
        ROOT.bell()
        # messagebox.showinfo('Incorrect input',
        #                     'The digits needs to be unique')
        return
    player_cur_result = computer.FindMatches(game_state.secret_number, guess)
    cur_round = game_state.round
    computer_cur_result = (game_state.computer_solution[cur_round-1][1],
                           game_state.computer_solution[cur_round-1][2])
    GUI.update_bulls_cows(player_cur_result, computer_cur_result)
    game_state.current_state = game_state.possible_states.INPROGRESS
    game_state.round += 1
    GUI.update_round(game_state.round)
    round_result = check_for_over(player_cur_result, computer_cur_result)
    if round_result is not None:
        GUI.game_result.config(text=round_result)
        game_state.current_state = game_state.possible_states.OVER


def check_for_over(player_stat, computer_stat):
    '''
    Checks if the game has ended
    '''
    if player_stat == (4, 0):
        return 'You have won!'
    if computer_stat == (4,0):
        return 'You have lost!'
    return None


def start_new_game(event, game_state):
    '''
    Checks the current state and starts new game
    '''
    if game_state.current_state == game_state.possible_states.START:
        GUI.reset_gui()
        main_game()
    elif game_state.current_state == game_state.possible_states.INPROGRESS:
        finish_game = messagebox.askquestion('Give up',
                                             'Do you want to give up?')
        if finish_game:
            GUI.reset_gui()
            main_game()
        return
    elif game_state.current_state == game_state.possible_states.OVER:
        GUI.reset_gui()
        main_game()


if __name__ == '__main__':
    ROOT = tk.Tk()
    GUI = GuiBuilder.BullsGui(ROOT)
    ROOT.resizable(width=False, height=False)
    main_game()
    ROOT.mainloop()
