# NBAFantasyMockDraft
Python script that runs a NBA fantasy draft simulation

This game is a simple version of ESPN’s NBA fantasy mock draft. Using python and the 2020 seaons data from basketball refernce, I created the worlds simplest mock draft. 

## Draft Instructions

*Please make sure NBA_fantasy_draft.py and nba_data.csv are in the same folder. Head over to terminal and run the program by entering NBA_fantasy_draft.py to start the draft.

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
9) At the end of the draft you can 
* View the players on the team,
* See the final standings
* Exit the game
