# Interactive Visualization Project - Dithered
### By Dieter Brehm and Jack Mao

## Overview
A project that uses Python to create an interactive visualization in the form of a roguelike rpg videogame.

## Setup
Uses the following python packages:  
* Pygame - Install using their installation instructions, but typically
`pip install pygame`

## Usage
run the game with `python3 main.py`

## Developing and Contributing
This project is developed using a pseudo-flow git model. Ideally, a new branch is
created for each and every new fairly significant feature. The process is as
follows:  
* Create new branch **from master** titled "feature: {}" where {} is a
  feat. name  
* Develop code using the relevant feature branch.  
	1.   `git checkout feature-{}` and `git merge master` at the start of coding sessions when
         possible. (Keeps the code fresh by making sure the feature is checked
         out and then merging master back in to the feature. This makes sure
         that that feature can always be easily merged back into master later.)  
	2.   commit any changes!  
* Merge work back into master through GitHub most likely.  
* Time for another feature!  
