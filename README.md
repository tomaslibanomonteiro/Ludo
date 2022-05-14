# Ludo 

Ludo is a Project developed for the subject Software Technology for Embedded Systems

## Description

The project consists of a simple boardgame (Ludo) played with 2 to 4 players. A Network arquitecture was developed so that the Game could be played with different players in different machines.

## Getting Started

### Dependencies

* The game was developed and tested in Ubuntu 20.04
* The game should run smoothly in other Linux distros but is known to cause Network connection problems in other environments like Windows 11

### Executing program

To start the game server, run the command: 

```
python run.py "IP_ADDRESS "PORT_NUMBER"
```

* If you don't give the IP and Port Number, the defaults in "setIPandPort.py" will be used

After getting the game server running, connect the first (Master) player, that will decide the base rules of the game (number of players, human pr pc player, etc) running the command

```
python client.py "IP_ADDRESS "PORT_NUMBER"
```

* Players must be in the same wifi network to play.


* The file "test_client.py" will send automatic messages to start the game with predefined options, run it instead if you want to automaticly start a predifined game.

After connecting the Master Player and set the rules for the game, wait until the rest of the human players connect to the game, by running the same command:

```
python client.py "IP_ADDRESS "PORT_NUMBER"
```


## Authors

Tomás Pereira de Brito Líbano Monteiro, tomasl00@gmail.com 
Ricardo Pacheco Café, ricardocafee00@gmail.com



