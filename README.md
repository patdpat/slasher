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

**So,What is The Win Condition of This Game**

    Super simeple, You suppress the frog population.

    Avoid making outrages frog-pocalypse,then you win!!

### Components Description

| Class        | Responsibility                                                       |
| ------------ | -------------------------------------------------------------------- |
| MyGame       | Start the app, store state, render screen, draw sprites, and update. |
| Player       | Handle user input, User character movement,update game.              |
| Frog         | Initialize obstacle frog, Frog movement,update game.                 |
| BouncingFrog | Handle bouncing mechanic, update game.                               |
| CircleFrog   | Handle orbitation mechanic, update game.                             |
| Heart        | Handle random spawning mechanic,Decreasing frog logic, update game.  |

**Game Development Idea**

    This game is inspired from Feeding Frenzy gameplay.The goal of this game is to survive as long as you can,

    While avoid hitting chracter that you should not supposed to hit.

### To Play This Game

    You have to install python and Arcade library, before clone the game to you computer.
