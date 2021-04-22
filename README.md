# NBADraft
Python script that runs a NBA fantasy draft simulation

This game is a simple version of ESPN’s NBA fantasy mock draft. Using python and the 2020 seaons data from basketball refernce, I created the worlds simplest mock draft. 

Draft Instructions

*Please make sure proj_1.py and nba_data.csv are in the same over. Head over to terminal and run the program by entering python proj_1.py to start the draft.
1) You will be promoted to enter the number of teams you want to create for the fantasy league. I have put guidelines in place to only allow 5-13 teams for each league. Entering any numbers otherwise will throw an error.
2) The program will randomly select a number from the total teams created, and that will be YOUR team. The other teams will be played by the computer.
3) You will them be asked if you want to start the game, enter 1 for yes, and 2 for no.
4) Depending on your draft position, the computers will either auto draft to your turn to
choose, or you will be prompted to make your pick. Note: auto draft = taking the first player
on the board.
5) When it is your turn to draft you can either enter 1 to select your own player (which will
show the draft board) or auto draft and take the first player available.
6) If you decide to draft your own player, the draft board will show up and you will be asked
which player you want to draft. You enter the rank of the player that you want to draft.
7) If you want to show a longer list of the board return 0, and it will ask you how big of the draft
board you want to view. (e.x. returning 75 will show 75 players on the board)
8) This process repeats for 13 rounds.
9) At the end of the draft you can 1) view the players on the team, 2) see the final standings, or
3) exit the game.
Challenges: One of the main challenges was understanding the structure of how the program would work. I needed to think of how I can create “x” about of Player objects and indexing them appropriately evetime I called their method. I eventually created a list of Player() classes that called a draft method every round. Additionally, cleaning the data initially to make it simple and readable for NP to work with was also a bit time consuming.
Additional features: In the future I would have the draft board rank the players by preseason and the final “fantasy scores” come from their end of season numbers. I thought of doing it this time around, but it was a lot of additional data cleaning that would need to be done. Additionally, I want to eventually add some AI/ML logic into the program. Knowing the corresponding stats to their fantasy values, I can create an optimal draft strategy for computer that would be hard to beat.
   
