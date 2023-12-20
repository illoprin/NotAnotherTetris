# Not Another Tetris
![Tetris Logo Light](https://github.com/illoprin/NotAnotherTetris/assets/145659467/f8c73d37-87d3-4082-ba0c-1e9404c923f9)
My own implemetntation of classical NES Tetris on Python
![Promo](https://github.com/illoprin/NotAnotherTetris/assets/145659467/37efc7c9-4369-4be0-b7aa-b445a5a83513)

# General Information
**The project is under development** Report all bugs and problems in the Issues section <br>
**Game has no sound controls!** Before starting, turn down the volume on the system. <br>

# Realization
Project graphics based on software CPU renderer from _**PyGame**_ library
<br>
#### Game Code Architecture
![Game Architecture](https://github.com/illoprin/NotAnotherTetris/assets/145659467/4382c90c-1f4a-4a36-a6e9-06e40c4444fe)

# Features
An attempt was made to take all the best mechanics from different variations of the Tetris game. You can see the examples below:
<br>
<br>
![Score Counter](https://github.com/illoprin/NotAnotherTetris/assets/145659467/dc1b8b3e-af12-4fb8-b3b5-cf08ca7a5d0c)
<br>
![Spin](https://github.com/illoprin/NotAnotherTetris/assets/145659467/22874315-109e-4804-a05b-4b57ac739bfe)
<br>
* You can change the ``debug`` boolean attribute on Controller instance to get access to debug mode. Here you can reflect tetrominoes and see the boundaries of the active and next figure
```main.py
controller = Controller(screen, True)
```
# Installation
Installation not needed. All you need to download latest release, but you need Python greater than 3.10 to launch the game.

# Plans
- **0.2 beta**
  - Improve tetromino rotation system
  - Add game level selection functionality
  - Add options menu with graphics and sound controls
- **0.2.5 beta**
  - Implement AI game mode

