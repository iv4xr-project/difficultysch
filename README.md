All these settings can be changed in settings.py

- To play the game manually change the variable AGENT to False

- To use an LRTA* agent to play the game set the variable AGENT to True
    
    The agent is stopped after 1000 runs where the agent gets to the goal

    While simulating u can use:
        -Key P to pause/unpause
        -Key R to remove/put the cap of 60 actions/sec (Default is on)
        -Key D to activate/remove drawing of the enviorment (Default is on)

    The variable NOISE can be changed from 0 to 1 to simulate an human error where its value represents the probability of a human error and a random action is chosen

    The variable ACTIONS represent the actions that the agent is capable of doing:
        0 - NOP
        1 - RIGHT
        2 - LEFT
        3 - JUMP
        4 - JUMP + RIGHT
        5 - JUMP + LEFT

        By default its [1,3,0]

-The map can be changed in the variable MAP and new maps can also be created:
    '1' - Floor
    'P' - Player (2 squares height)
    'F' - Flag (8 squares height)
    '2' - Pipe (2 squares height)
    '.' - used to simulate empty

    Maps can have any height and width but the reccomended height is 13 squares
