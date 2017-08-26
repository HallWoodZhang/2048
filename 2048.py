#!/usr/bin/env python
# coding=utf-8

import curses
from Fielder import *


def main(stdscr):

    def init():
        # init the panel
        gameField.reset()
        return 'Game'

    def notGame(state):
        # print GameOver panel
        gameField.draw(stdscr)
        # get the action, then response the input
        action = getAction(stdscr)
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'
        return responses[action]

    def Game():

        gameField.draw(stdscr)
        action = getAction(stdscr)

        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if gameField.move(action):  # move successfully
            if gameField.isWin():
                return 'Win'
            if gameField.isGameOver():
                return 'GameOver'
        return 'Game'

    stateActions = {
        'Init': init,
        'Win': lambda: notGame('Win'),
        'GameOver': lambda: notGame('GameOver'),
        'Game': Game

    }

    state = 'Init'

    gameField = GameField(win=2048)
    curses.use_default_colors()

    state = 'Init'

    while state != 'Exit':
        state = stateActions[state]()

curses.wrapper(main)