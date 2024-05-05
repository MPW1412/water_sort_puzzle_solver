#!/usr/bin/env python3
from copy import deepcopy
import sys

TUBE_HEIGHT = 4


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
        'P': (176, 89, 193)
    }

    def __init__(self, fluids):
        self.height = TUBE_HEIGHT
        self.fluids = fluids

    def __str__(self):
        overline = '\u203E'
        formatted_fluids = []
        for _ in range(self.height - len(self.fluids)):
            formatted_fluids.append('|    |')

        for fluid in reversed(self.fluids):
            color = self.COLORS.get(fluid.strip(), (0, 0, 0)) 

            rgb_code = ';'.join(map(str, color))
            formatted_fluid = f'\033[48;2;{rgb_code}m|    |\033[0m'
            formatted_fluids.append(formatted_fluid)

        formatted_fluids.append('\u203E' * 6)
#        formatted_fluids.append(str(len(self.fluids)) + '\u203E' * 5)

        return '\n'.join(formatted_fluids)

    def pourIn(self, tube: 'Tube'):
        if not tube.fluids:
            return False
        if not self.fluids and all(x == tube.fluids[0] for x in tube.fluids):
            return False # prevent useless step
        if tube.fluids[-1] not in self.COLORS:
            raise ValueError("Unknown Colour Exception")
        if len(self.fluids) == self.height:
            return False
        if not self.fluids or self.fluids[-1] == tube.fluids[-1]:
            self.fluids.append(tube.fluids.pop())
            self.pourIn(tube)
            return True
        return False

    def completed(self) -> bool:
        return not self.fluids or (len(self.fluids) == self.height and all(x == self.fluids[0] for x in self.fluids))

    def compstring(self) -> str:
        return ''.join(self.fluids) + 'X' * (self.height - len(self.fluids))
        
        
class Game:
    def __init__(self, num_tubes, parent = None):
        self.num_tubes = num_tubes
        self.parent = parent
        self.tubes = []

    def addTube(self, tube):
        if len(self.tubes) < self.num_tubes:
            self.tubes.append(tube)
        else:
            raise GameFullError("Game is full, cannot add more tubes")

    def completed(self) -> bool:
        return all(tube.completed() for tube in self.tubes)

    def gameset(self) -> str:
        return ''.join([tube.compstring() for tube in self.tubes])

    def __eq__(self, other):
        if isinstance(other, Game):
            return self.gameset() == other.gameset()
        return NotImplemented

# Beispiel Verwendung:
game = Game(14)
game.addTube(Tube(['HB', 'P', 'T', 'R']))
game.addTube(Tube(['HG', 'R', 'B', 'HB']))
game.addTube(Tube(['R', 'G', 'O', 'GR']))
game.addTube(Tube(['HB', 'L', 'RO', 'B']))
game.addTube(Tube(['P', 'P', 'L', 'B']))
game.addTube(Tube(['DG', 'G', 'O', 'T']))
game.addTube(Tube(['L', 'DG', 'T', 'O']))
game.addTube(Tube(['RO', 'GR', 'O', 'P']))
game.addTube(Tube(['G', 'RO', 'T', 'GR']))
game.addTube(Tube(['HG', 'R', 'B', 'GR']))
game.addTube(Tube(['HG', 'DG', 'L', 'DG']))
game.addTube(Tube(['HG', 'RO', 'G', 'HB']))
game.addTube(Tube([]))
game.addTube(Tube([]))

#game = Game(5)
#game.addTube(Tube(['R', 'B', 'R', 'B']))
#game.addTube(Tube(['B', 'G', 'G', 'B']))
#game.addTube(Tube(['G', 'G', 'R', 'R']))
#game.addTube(Tube([]))
#game.addTube(Tube([]))

def print_tubes(tubes):
    num_tubes = len(tubes)
    num_groups = (num_tubes + 6) // 7

    for i in range(num_groups):
        start_idx = i * 7
        end_idx = min((i + 1) * 7, num_tubes)
        
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
    print('=' * 80)
    print('Solution: ')
    solution.append(game)
    lineup_solution_path(game)
    for i in range(len(solution)):
        print(f"Step {i}:")
        print_tubes(solution[i].tubes)
        
    sys.exit(0)

def lineup_solution_path(game: 'Game'):
    if game.parent:
        solution.insert(0, game.parent)
        lineup_solution_path(game.parent)

games = [game]
gameset_history = []
gameset_history.append(games[0].gameset())
solution = []

print_tubes(games[0].tubes)

while games:
    parent_game = games.pop()
    child_game = deepcopy(parent_game)
    child_game.parent = parent_game
    for i in range(parent_game.num_tubes):
        for x in range(parent_game.num_tubes):
            if i == x:
                continue
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