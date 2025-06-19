from flask import Flask, request, jsonify

app = Flask(__name__)

class Board:
    def __init__(self, length: int, width: int, board: list, end_square=(0, 4)):
        self.length = length
        self.width = width
        self.board = board
        self.end_square = end_square

    def isWinningBoard(self):
        visited = [[False] * self.width for _ in range(self.length)]
        return self.checkFlow(*self.end_square, visited)

    def checkFlow(self, x: int, y: int, visited: list):
        if not (0 <= x < self.length and 0 <= y < self.width):
            return False
        if visited[x][y]:
            return True  # Already visited
        visited[x][y] = True
        
        # Check if we reached the end square
        if (x, y) == self.end_square:
            return True
        
        # Check the flow direction
        flow = self.board[x][y]
        if flow == 1:  # Up
            return self.checkFlow(x - 1, y, visited)
        elif flow == 2:  # Down
            return self.checkFlow(x + 1, y, visited)
        elif flow == 3:  # Left
            return self.checkFlow(x, y - 1, visited)
        elif flow == 4:  # Right
            return self.checkFlow(x, y + 1, visited)

        return False  # Invalid flow

@app.route('/check_board', methods=['POST'])
def check_board():
    data = request.json
    length = data.get('length')
    width = data.get('width')
    end_square = data.get('end_square', [0, 4])  # Default is top-right corner
    board_config = data.get('board')

    if not isinstance(board_config, list) or len(board_config) != length or any(len(row) != width for row in board_config):
        return jsonify({"error": "Invalid board configuration."}), 400

    # Create the board object
    board = Board(length, width, board_config, tuple(end_square))
    
    # Check if it's a winning board
    is_winning = board.isWinningBoard()
    return jsonify({"winning": is_winning})

if __name__ == '__main__':
    app.run(debug=True)
