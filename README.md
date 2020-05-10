# DCauto
Python-based automation for Destiny Child game on Android

Working on LD Player with 460x860 resolution

Small automation project i did to play Destiny Child game.
Why? because this game give a LOT of stamina to do mission with. And those mission unskippable. While the auto farming existing inside the game is already good enough, it doesn't provide auto farming on big event. Such as:
- World Boss mode
- Ragna Break (Raid Boss)
These event are very time consuming since the battle phase is unskippable, and usually you need 1x speed for maximum damage output (using 3x speed is lowering your FPS, hence lowering your child's DPS).

World Boss mode (wb_auto.py)
Last updated on World Boss Khepri.
- Counts how many raid you done.
- Capable to auto buy new raid ticket (using 2k crystal. Disable it if you don't want to spend crystal)
- Can go idle, waiting for new ticket countdown.

Ragna Break Raid Boss (Isolde_auto.py)
Last updated on Summer Spike Isolde event.
- Fully automated Battle Phase.
- Able to search best raid boss (looking for beatable raid boss with alot of player count)
- Can read raid ticket amount, count raid amount

This automation running for around 15 hour (yes, that's how tedious this game is) a day helped me stayed on Top100 in the event while spending no money at all.

How to use:
Use any python compiler to run the file you need.

Dependencies:
OpenCV

You might need to update the IMG folder for latest event update. I stopped working on this since i retired from the game.
