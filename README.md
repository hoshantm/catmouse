# catmouse
Game of Cat and Mouse

This is a further analysis of the solution of the Game of Cat and Mouse - Numberphile puzzle described on YouTube (https://www.youtube.com/watch?v=vF_-ob9vseM&t=385s). It addresses two areas:

- Initial conditions that allow a straight line escape
- Optimum spiral path equation prior to "dash" escape

Extensive comments are provided in the Python code to explained what is being done. The code is not optimal but is sufficient for the purpose of providing a useful analysis.

Edit - 09/30/2019
Added catmouse_game.py that simulates the pursuit with a limit of 4.33 cat to mouse speed ratio for the mouse to escape. number is accurate to about 5E-3 due to rounding errors. Note that pygame needs to be installed by typing the following command:
pip install pygame
