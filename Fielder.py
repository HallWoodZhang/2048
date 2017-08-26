from random import randrange, choice
from collections import defaultdict

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letterCodes = [ord(ch) for ch in 'WASDRQwasdrq']
actions_dict = dict(zip(letterCodes, actions * 2))

def getAction(keyboard):
    char = 'N'
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]

# transpose the martrix
def transpose(field):
    return [list(row) for row in zip(*field)]

# invert the martrix
def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self, height = 4, width = 4, win = 2048):
        self.height = height
        self.width = width
        self.winVal = win
        # you win the game when you reach 2048
        self.score = 0
        self.highscore = 0
        self.field = []
        self.reset()

    def spawn(self):
        newElem = 4 if randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in xrange(self.width) for j in xrange(self.height) if self.field[i][j] == 0])
        self.field[i][j] = newElem

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in xrange(self.width)] for j in xrange(self.height)]
        self.spawn()
        self.spawn()


    def move(self, dirc):
        def moveRowToLeft(row):

            def tighten(row): # squeese non-zero elements together
                newRow = [i for i in row if i != 0]
                newRow += [0 for i in xrange(len(row) - len(newRow))]
                return newRow

            def merge(row):
                pair = False
                newRow = []
                for i in xrange(len(row)):
                    if pair:
                        newRow.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            newRow.append(0)
                        else:
                            newRow.append(row[i])
                assert len(row) == len(newRow)
                return newRow

            return tighten(merge(tighten(row)))

        # magic!!!
        moves = {}
        moves['Left'] = lambda field: [moveRowToLeft(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

        if dirc in moves:
            if self.movable(dirc):
                self.field  = moves[dirc](self.field)
                self.spawn()
                return True
            else:
                return False

    def isWin(self):
        return any(any(i >= self.winVal for i in row) for row in self.field)

    def isGameOver(self):
        return not any(self.movable(move) for move in actions)

    def movable(self, dirc):
        def rowLeftMovable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i + 1] == row[i]:
                    return True
                return False

            return any(change(i) for i in xrange(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(rowLeftMovable(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))

        if dirc in check:
            return check[dirc](self.field)
        else:
            return False

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'

        def cast(string):
            screen.addstr(string + '\n')

        def drawSeperator():
            line = '+' + ('+------' * self.width + '+')[1:]
            seperator = defaultdict(lambda: line)
            if not hasattr(drawSeperator, "counter"):
                drawSeperator.counter = 0
            cast(seperator[drawSeperator.counter])
            drawSeperator.counter += 1

        def drawRow(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))
        for row in self.field:
            drawSeperator()
            drawRow(row)
        drawSeperator()
        if self.isWin():
            cast(win_string)
        else:
            if self.isGameOver():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)
