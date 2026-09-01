# Evade

A game I just made for fun :) Hopefully you enjoy

A survival game where you dodge bouncing balls for as long as possible.

## How to Play

- Control your yellow ball with your mouse cursor
- Avoid the colorful balls that spawn from the edges
- Survive as long as you can — your score increases every second
- The screen gets more chaotic as balls accumulate!

## Features

- **Size-speed scaling:** Big balls are slow, small balls are fast
- **Local high score tracking** (web version)
- **Progressive difficulty:** More balls = less safe space
- **Refresh-rate independent movement** (web version): Uses delta-time scaling so gameplay speed stays consistent whether you're on a 60Hz or 144Hz+ monitor

## Play

**Web version:** [Play Evade](https://owenlatt9.github.io/game.html)

**Python version:** Requires Python 3 with tkinter (included in most standard Python installs)
```bash
python evade.py
```

## Files

| File | Description |
|------|--------------|
| `evade.py` | Original Python/Tkinter version of the game |
| `game.html` | Web version built with HTML5 Canvas and vanilla JavaScript, including persistent high score via `localStorage` |

## Tech Used

- **Python version:** Tkinter (Canvas API) for rendering, `root.after()` for the game loop
- **Web version:** HTML5 Canvas, vanilla JavaScript, `requestAnimationFrame` for the game loop, `localStorage` for high score persistence
