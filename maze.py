from flask import Flask, render_template
import random

app = Flask(__name__)

@app.route('/')
def index():
    maze = [[' ' for _ in range(7)] for _ in range(7)]
    maze[0][0] = 'static/door.png' 
    maze[6][6] = 'static/flag.png'  

    skulls_to_place = 16
    while skulls_to_place > 0:
        row = random.randint(0, 6)
        col = random.randint(0, 6)
        if maze[row][col] == ' ': 
            maze[row][col] = 'static/bhooth.png'
            skulls_to_place -= 1
            
    return render_template('index.html', maze=maze)

if __name__ == '__main__':
    app.run(debug=True)
