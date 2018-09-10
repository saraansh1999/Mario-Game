# MARIO GAME

Created By : Saraansh Tandon
<br/><br/><br/>

---------------------------

### ABOUT
>Mario is a very popular game which originated first in 1980s.
>This is a terminal based minimal clone of the game.

---------------------------

### RULES

>* The player controls the character of Mario.

>* The player goes along in the game while fighting different types of enemies , colecting rewards and powerups to finall fight the boss.

>* The player gets 3 lives in which they have to complete the game by successfully killing the Boss who has 10 lives.

>* The player can lose a life due to
	* Falling in a Pit
	* Colliding with an enemy or boss or their bullets.

>* The player can shoot only after they have collected the Gun powerup.

>* All enemies other than the boss have single lives.

>* Score is calculated by rewarding 5 points for each coin collected and 20 points for each enemy/boss life taken.

---------------------------

### STARTING THE GAME

> Just download/clone the game files and run the following :  ```$ python3 main.py```
---------------------------

### CONTROLS

>* 'w' to Jump
>* 'd' to Move Right
>* 'a' to Move Left
>* 'g' to Shoot(directed towards the side Mario last moved, i.e. left or right)
>* '0' to Quit (Zero)

---------------------------

### DESCRIPTION OF CLASSES USED

>* **Screen** class is used to create the playing environment background board

>* **Scoreboard** class is used to keep a track of the scores and lives left.

>* **Player** class is used to create and control the movements of **Mario**

>* **Enemy** class is inherited by three other class to create and control different kinds of enemies. They also check for collisions of enemies with various things like bullets, Mario etc.

>* **Elements** class in environmeny.py is used to specify and control various objects present in the game like : 
	>* Pipes
	>* Brick Bridges
	>* Vertically moving bridges
	>* Springs
	>* Pits
	>* Bullets of all kinds
	>* Clouds	

>* Almost all of the environment elements have a **Maker** class in 'environment_maker.py' which is responsible for creating those objects.

>* **Collectibles** class is used to create all the collectible items.The **Coins** and **Gun Powerups** are created by inheriting from this class.

>* **getChUnix** class is used to enable the game to read input from the user.

---------------------------

### Note

> Works best in `python3.6`

