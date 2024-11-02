from flask import Flask, render_template
import random

app = Flask(__name__)

def is_valid_move(x, y, visited, maze):
    return (0 <= x < 7 and 0 <= y < 7 and 
            (x, y) not in visited and 
            maze[x][y] != 'static/bhooth.png')

def has_path_to_end(maze, start=(0,0), end=(6,6)):
    visited = set()
    stack = [(start[0], start[1])]
    
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while stack:
        current = stack.pop()
        if current == end:
            return True
            
        if current not in visited:
            visited.add(current)
            
            for move in moves:
                next_x = current[0] + move[0]
                next_y = current[1] + move[1]
                
                if is_valid_move(next_x, next_y, visited, maze):
                    stack.append((next_x, next_y))
    
    return False

@app.route('/')
def index():
    while True:  
        maze = [[' ' for _ in range(7)] for _ in range(7)]
        
        maze[0][0] = 'static/door.png'
        maze[6][6] = 'static/flag.png'
        
        skulls_to_place = 16
        attempts = 0
        max_attempts = 100  
        
        while skulls_to_place > 0 and attempts < max_attempts:
            row = random.randint(0, 6)
            col = random.randint(0, 6)
            
            if (row, col) not in [(0,0), (6,6)] and maze[row][col] == ' ':
                maze[row][col] = 'static/bhooth.png'
                
                if has_path_to_end(maze):
                    skulls_to_place -= 1
                else:
                    maze[row][col] = ' '
                    
            attempts += 1
        
        if skulls_to_place == 0:
            break
    
    return render_template('index.html', maze=maze)

if __name__ == '__main__':
    app.run(debug=True)