from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
from dataclasses import dataclass
import numpy as np
import random
import pickle
from pathlib import Path

FLAG = "NTO{no_minotaurus_here}"


@dataclass
class MyMaze:
    maze: np.ndarray
    start: tuple[int, int]
    end: tuple[int, int]
    solution: list[tuple[int, int]]


mazes: list[MyMaze] = []
main: str = open("main.html").read()

print("Checking cache")
if Path("cache/mazes.pkl").is_file():
    f = open("cache/mazes.pkl", "rb")
    mazes = pickle.loads(f.read())
    print("Cache hit")
else:
    print("Cache miss")
    print("Generating mazes...")
    for i in range(7):
        print(f"Generating maze {i}", end="\n")
        m = Maze()
        m.generator = Prims(100, 100)
        m.generate()
        m.generate_entrances()
        print(f"Solving maze {i}")
        m.solver = BacktrackingSolver()
        m.solve()
        solution = [m.start, *m.solutions[0], m.end]
        m.grid[m.end] = 0

        maze = MyMaze(m.grid, m.start, m.end, solution)
        mazes.append(maze)
    print("\n")
    print("Caching mazes")
    f = open("cache/mazes.pkl", "wb")
    f.write(pickle.dumps(mazes))

app = FastAPI()


@app.get("/")
async def root():
    return HTMLResponse(main)


def get_possible_moves(grid: np.ndarray, position: tuple[int, int]):
    # returns list of possible moves: ["up", "left"] for example
    # in grid 1 is wall, 0 is empty
    x, y = position
    moves = []
    if x > 0 and grid[x - 1][y] == 0:
        moves.append("up")
    if x < len(grid) - 1 and grid[x + 1][y] == 0:
        moves.append("down")
    if y > 0 and grid[x][y - 1] == 0:
        moves.append("left")
    if y < len(grid[0]) - 1 and grid[x][y + 1] == 0:
        moves.append("right")
    return moves


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    current_maze = random.choice(mazes)
    print(current_maze.solution)
    print(current_maze.maze)

    possible_moves = get_possible_moves(current_maze.maze, current_maze.start)
    await websocket.send_json(
        {
            "position": current_maze.start,
            "end": current_maze.end,
            "possible_moves": possible_moves,
            "status": "start",
        }
    )

    position = current_maze.start

    move_map = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    while True:
        move = (await websocket.receive_text()).strip()
        if move not in possible_moves:
            await websocket.send_json(
                {
                    "status": "invalid move",
                    "position": position,
                    "possible_moves": possible_moves,
                    "end": current_maze.end,
                }
            )
            continue

        position = (
            position[0] + move_map[move][0],
            position[1] + move_map[move][1],
        )
        if position == current_maze.end:
            await websocket.send_json(
                {
                    "status": FLAG,
                    "position": position,
                    "end": current_maze.end,
                    "possible_moves": [],
                }
            )
            break

        possible_moves = get_possible_moves(current_maze.maze, position)
        await websocket.send_json(
            {
                "position": position,
                "end": current_maze.end,
                "possible_moves": possible_moves,
                "status": "ok",
            }
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
