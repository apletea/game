import numpy as np

class GameLoop:

    def __init__(self, w, h, players):

        self.h = h
        self.w = w
        self.players = players
        self.game_field = np.zeros((w,h), dtype=np.int8)
        self.game_field = self.game_field - 1

    def _check(self, array: np.array) -> bool:
        if (len(array) != 4):
            return False
        var = array.var()
        mean = array.mean()
        if np.isclose(var, 0) and not np.isclose(mean, -1) :
            return True
        return False
        
    def _isend(self) -> bool:
        for i in range(self.w):
            for j in range(self.h):
                if self._check(self.game_field[i:i+4,j]):
                    self.solution = [(k,j) for k in range(i, i+4)]
                    return True
                if self._check(self.game_field[i,j:j+4]):
                    self.solution = [(i,k) for k in range(j, j+4)]
                    return True
                if (i+4) < self.h and (j+4) < self.w:
                    diagonal = np.array([self.game_field[i+k][j+k] for k in range(4)])
                    if self._check(diagonal):
                        self.solution = [(i+k,j+k) for k in range(4)]
                        return True
                if (i-4) > 0 and (j+4) < self.w:
                    diagonal = np.array([self.game_field[i-k][j+k] for k in range(4)])
                    if self._check(diagonal):
                        self.solution = [(i-k,j+k) for k in range(4)]
                        return True

        return False

    def _solution(self) -> list:
        return self.solution

    def _isvalid(self, column: int) -> bool:
        if column >= self.h or column < 0:
            return False
        column_val = self.game_field[:, column]
        mask = np.where(column_val == -1)
        if mask[0].size == 0:
            return False
        return True
    
    def _add_to_column(self, column: int, player_id: int) -> None:
        column_val = self.game_field[:, column]
        mask = np.where(column_val == -1)
        next_index = mask[0][-1]
        self.game_field[next_index, column] = player_id
        

    def _next_turn(self, player_id: int) -> None:
        print(f'Turn of player: {player_id}')
        _valid = False
        while not _valid: 
            column = int(input("Enter a valid column:"))
            _valid = self._isvalid(column)
        self._add_to_column(column, player_id)

    def _visualize(self) -> None:
        print(self.game_field)

    def run(self) -> None:

        player_id = 0
        _end = self._isend()
        while not _end:
            self._next_turn(player_id)
            player_id = (player_id + 1) % self.players
            self._visualize()
            _end = self._isend()
        winner = (player_id + self.players - 1) % self.players
        solution = self._solution()
        print("winner", winner)
        print("solution", solution)


    

if __name__=="__main__":
    game = GameLoop(6,7,2)
    game.run()