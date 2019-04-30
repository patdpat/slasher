### Slasher : Juke The Frogs

![alt text](https://raw.githubusercontent.com/patdpat/slasher/master/images/frog/frog1.png)
![alt text](https://raw.githubusercontent.com/patdpat/slasher/master/images/frog/frog4.png)

    Computer Programming 2 Final Project

    Simple Game using Python and Arcade Library

### How to Play

1.  Move Character with Keyboard

2.  You win by decrese number of frog to become less than 5

3.  You lose by increase number of frog to become more than 200

4.  Floating Melon decrease amount of frogs by 5 per 1 melon hit

5.  For every 5 frogs you hit, You'll be punished by getting 6 more frogs

### Description

| Class        | Responsibility                                                       |
| ------------ | -------------------------------------------------------------------- |
| MyGame       | Start the app, store state, render screen, draw sprites, and update. |
| Player       | Handle user input, update game.                                      |
| Frog         | Handle obstacle frog, update game.                                   |
| BouncingFrog | Handle bouncing mechanic, update game.                               |
| CircleFrog   | Handle orbitation mechanic, update game.                             |
| Heart        | Handle random spawning, update game.                                 |
