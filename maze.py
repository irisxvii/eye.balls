from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    grid_size = 5
    maze = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]
    return render_template('index.html', maze=maze)

if __name__ == '__main__':
    app.run(debug=True)
