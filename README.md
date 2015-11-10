#A Puzzling World

This challenge focuses on using Pygame's mixer to add music and sound effects. The provided code allows the user to select a regional world map, 
creates a jigsaw puzzle from the image and allows the user to connect pieces to assemble the puzzle.

Github repo: https://github.com/reddit-pygame/puzzle-challenge

Reddit Challenge post: https://www.reddit.com/r/pygame/comments/3s9m2j/challenge_a_puzzling_world/

##How It Works

The puzzle is created by taking subsurfaces from the map image, centering them onto a larger surface and overlaying the correct puzzle piece. The pieces were 
were similarly created from resources\graphics\puzzle.png. The black portions were done manually in paint.net.

The user can grab or place a piece or section of pieces by left-clicking the mouse. Placing a piece or section next to a neighboring piece or section joins the pieces/sections 
(when the puzzle is completed there will be a single PuzzleSection object that contains all the puzzle pieces).

##Controls

**Left-click** Grab/place pieces

**F** Toggle fullscreen

**ESC** Exit

###Challenge

Add music: There are two songs in prepare.MUSIC, "sombrero" and "tropical". When one song finishes the next song should start playing.

Add sound: There is a Sound object (prepare.SFX["connect"]) which should be played whenever pieces or sections are joined together.


##Some Links

[pygame.mixer.Sound](https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound)

[pygame.mixer.music](https://www.pygame.org/docs/ref/music.html)

[itertools.cycle](https://docs.python.org/2/library/itertools.html#itertools.cycle)

[OpenGameArt](http://opengameart.org/)

[freesound.org](https://www.freesound.org/)

##Achievements

**Get Off My Lawn** - Allow the user to turn music off

**A Poor Beautician** - Implement a timer that displays how long the user has been working on the puzzle. The timer should start when the user picks a map and stop when the puzzle is complete.

**Sweet Sound of Success** - Find a sound effect to play when the user completes the puzzle.

