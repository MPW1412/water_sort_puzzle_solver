#!/usr/bin/env python3
from copy import deepcopy
import math
import sys

TUBE_HEIGHT = 4
# Prevent pouring, if receiving tube can't receive all of it
# Shortens solution path by preventing unnecessary forth and back pouring
# I'm quite sure this does not break anything, but not 100%.
SPEED_OPTION = True


class GameFullError(Exception):
    pass

class Tube:
    COLORS = {
        'R': (180, 58, 57),
        'HG': (103, 170, 13),
        'B': (0, 37, 203),
        'T': (0, 230, 166),
        'RO': (220, 104, 125),
        'G': (255, 230, 65),
        'O': (217, 130, 53),
        'L': (104, 47, 142),
        'GR': (112, 112, 112),
        'HB': (85, 163, 229),
        'DG': (57, 82, 16),
        'P': (176, 89, 193),
        '?': (255, 255, 255)
    }

    def __init__(self, fluids):
        self.height = TUBE_HEIGHT
        self.fluids = fluids
        self.flag_in = False
        self.flag_out= False

    def __str__(self):
        overline = '\u203E'
        formatted_fluids = []
        s = '  '
        if self.flag_in:
            s = 'vv'
        if self.flag_out:
            s = '^^'
        for _ in range(self.height - len(self.fluids)):
            formatted_fluids.append(f'| {s} |')
            s = '  '

        for fluid in reversed(self.fluids):
            color = self.COLORS.get(fluid.strip(), (0, 0, 0)) 

            rgb_code = ';'.join(map(str, color))
            
            formatted_fluid = f'\033[48;2;{rgb_code}m| {s} |\033[0m'
            s = '  '
            formatted_fluids.append(formatted_fluid)

        formatted_fluids.append('\u203E' * 6)
#        formatted_fluids.append(str(len(self.fluids)) + '\u203E' * 5)

        return '\n'.join(formatted_fluids)

    def pourIn(self, tube: 'Tube'):
        if not tube.fluids:
            return False
        if not self.fluids and all(x == tube.fluids[0] for x in tube.fluids):
            return False # prevent useless step
        if tube.fluids[-1] == '?':
            return False
        if tube.fluids[-1] not in self.COLORS:
            raise ValueError("Unknown Colour Exception")
        if len(self.fluids) == self.height:
            return False
        if not self.fluids or self.fluids[-1] == tube.fluids[-1]:
            if SPEED_OPTION and self.fluids:
                r = 1
                while len(tube.fluids) > r + 1 and tube.fluids[-r-1] == self.fluids[-1]:
                    r += 1
                
                if r > 1 and (len(self.fluids) + r) >= self.height:
                    return False
            self.fluids.append(tube.fluids.pop())
            self.pourIn(tube)
            return True
        return False

    def completed(self) -> bool:
        return not self.fluids or (len(self.fluids) == self.height and all(x == self.fluids[0] for x in self.fluids))

    def compstring(self) -> str:
        return ''.join(self.fluids) + 'X' * (self.height - len(self.fluids))
        
        
class Game:
    def __init__(self):
        self.num_tubes = 0
        self.parent = None
        self.tubes = []

    def addTube(self, tube):
        self.tubes.append(tube)
        self.num_tubes += 1

    def completed(self) -> bool:
        return all(tube.completed() for tube in self.tubes)

    def gameset(self) -> str:
        return ''.join([tube.compstring() for tube in self.tubes])

    def __eq__(self, other):
        if isinstance(other, Game):
            return self.gameset() == other.gameset()
        return NotImplemented

def print_tubes(tubes):
    num_tubes = len(tubes)
    num_per_row = math.ceil(num_tubes / 2)
    num_groups = (num_tubes + num_per_row - 1) // num_per_row

    for i in range(num_groups):
        start_idx = i * num_per_row
        end_idx = min((i + 1) * num_per_row, num_tubes)
        
        group_strings = [str(tube) for tube in tubes[start_idx:end_idx]]

        for j in range(len(group_strings[0].split('\n'))):
            print('  '.join(group_string.split('\n')[j] for group_string in group_strings))
        print()
    print('-' * 60)
    print()

def set_cursor_and_print_tubes(tubes):
    sys.stdout.write('\033[14A')
#    sys.stdout.write('\033[8A')
    sys.stdout.flush()
    print_tubes(tubes)

def solution_found(game: 'Game'):
    solution = []
    print('=' * 80)
    print('Solution: ')
    solution.append(game)
    lineup_solution_path(game, solution)
    for i in range(len(solution)):
        if i > 0:
            for x in range(len(solution[i].tubes)):
                if len(solution[i].tubes[x].fluids) > len(solution[i-1].tubes[x].fluids):
                    solution[i].tubes[x].flag_in = True
                if len(solution[i].tubes[x].fluids) < len(solution[i-1].tubes[x].fluids):
                    solution[i].tubes[x].flag_out = True
        print(f"Step {i}:")
        print_tubes(solution[i].tubes)
        
    sys.exit(0)

def lineup_solution_path(game: 'Game', solution):
    if game.parent:
        solution.insert(0, game.parent)
        lineup_solution_path(game.parent, solution)


    
def solve(game: 'Game'):
    games = [game]
    gameset_history = []
    gameset_history.append(games[0].gameset())
    
    print_tubes(games[0].tubes)
    
    while games:
        parent_game = games.pop()
        child_game = deepcopy(parent_game)
        child_game.parent = parent_game
        for i in range(parent_game.num_tubes):
            for x in range(parent_game.num_tubes):
                if i == x:
                    continue
                if child_game.tubes[i].fluids and child_game.tubes[i].fluids[-1] == '?':
                    solution_found(child_game)
                if child_game.tubes[x].pourIn(child_game.tubes[i]):
                    if not child_game.gameset() in gameset_history:
                        games.append(child_game)
                        gameset_history.append(child_game.gameset())
                        set_cursor_and_print_tubes(child_game.tubes)
                        #print_tubes(child_game.tubes)
                        if child_game.completed():
                            solution_found(child_game)
                    child_game = deepcopy(parent_game)
                    child_game.parent = parent_game
                        
    print('No solution found!')
    sys.exit(1)

def main():
    game = Game()
    game.addTube(Tube(['T', 'L', 'HG', 'DG']))
    game.addTube(Tube(['?', '?', 'DG', 'R']))
    game.addTube(Tube(['?', '?', 'G', 'O']))
    game.addTube(Tube(['?', '?', 'O', 'HG']))
    game.addTube(Tube(['?', '?', '?', 'P']))
    game.addTube(Tube(['B', 'T', 'T', 'B']))
    game.addTube(Tube(['?', '?', 'GR', 'HG']))

    game.addTube(Tube(['?', '?', 'R', 'T']))
    game.addTube(Tube(['?', '?', '?', 'G']))
    game.addTube(Tube(['?', 'L', 'HB', 'G']))
    game.addTube(Tube(['?', '?', '?', 'O']))
    game.addTube(Tube(['?', '?', 'R', 'B']))
    game.addTube(Tube([  ]))
    game.addTube(Tube([  ]))

    solve(game)
    
if __name__ == '__main__':
    main()
