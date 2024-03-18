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

>**Note:** There are other version with more than two cell states but we are sticking to the two state version(*cause it;s easy*)~:smily:
