# Conway's Py Life

This project is simple(toy) replication of more complex and advance implementations of [Conway's Game Of Life simulation](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).\
The project is built using :-\
[![python](https://legacy.python.org/community/logos/python-logo.png)](https://www.python.org)
[![pygame](https://www.pygame.org/docs/_images/pygame_tiny.png)](https://pygame.org)

# About Simulation

Conway's Game Of Life is zero player game which doesn't need any user interaction once started. Simulation takes one time input as pattern and further evolve based on a set of rules ,i.e, :-
- A cell will live on only if there are 2 or 3 live neighbours.
- A cell will born if it has exactly 3 live neighbours.
- A cell will die if it has more than 3 neighbours,
- A cell will die if it has less than 2 neighnours.

Conway's game of life version have only two cell states ,i.e, :-
- live
- dead
>**Note:** There are other version with more than two cell states but we are sticking to the two state version(*cause it;s easy*&#128077;)

# Dependency

Since the code is in python you would need to install python in your system if not installed already.
### ***Linux***
Simple way
```bash
apt install python3
```
or try\
[Linux installation](https://www.python.org/downloads/source/)

### ***Windows***
use standalone installer or whatever you wish\
[Windows Installation](https://www.python.org/downloads/windows/)

### ***Mac***
use standalone installer or whatever you wish\
[MacOs Installation](https://www.python.org/downloads/macos/)

After installing python run this command
```bash
cd conways_life_game
pip3 install -r requirement.txt
```
Now simply run the python script

**linux**
```bash
python3 conways_game_o_life.py
```
**windows**
```bash
python conways_game_o_life.py
```
# Key Binds

- Simple mouse based pattern drawing system.
- <kbd>SPACE</kbd> for Start/Stop/Continue/Pause.
- <kbd>BACKSPACE</kbd> for Canvas reset.
- /Rest is gui (*melody khao khud jaan jao*)

<br>
<br>

<STRONG style="font-size:3em;">THANKS FOR STOPPING BY :)❤️</strong>