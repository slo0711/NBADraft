import pandas as pd
import numpy as np
import sys
import random


class Files():
    '''class to load the files into the program'''

    def __init__(self, data):
        self.data = data

    def read_data(self):
        data = pd.read_csv(self.data)
        return data

    def __repr__(self):
        return repr(self.data)


class DraftBoard():
    '''class that loads a parent class Files. This will do multiple methods such as creating the board, removing
    a player from the board etc...'''

    def __init__(self, files):
        self.files = files
        self.files = self.files.read_data()

    # this function drops the player from the draft board when a player is drafted
    # input will be the rank from the user inpit
    def draft_player(self, rank):
        self.files = self.files[self.files.RK != rank]

    # returns the current draft board with the top 50 players to choose from
    def show_board(self):
        print(self.files[['RK', 'NAME','PTS','REB','AST','BLK','STL','3PM',
                         'TO', 'DD2','TD3']].head(49).to_string(index=False))

    # will show the draftboard, depending on what the input is for the top x amount of players
    def show_board_input(self, num):
        print(self.files[['RK', 'NAME','PTS','REB','AST','BLK','STL','3PM',
                         'TO', 'DD2','TD3']].head(num - 1).to_string(index=False))

    # returns the rank of the first player on the draft board. This will be used for autodraft teams
    def get_rank_first_row(self):
        return self.files['RK'].iloc[0]

    # returns the first name of the player on the draft board
    def get_first_player_name(self):
        return self.files['NAME'].iloc[0]

    # returns a list of all the Rk's of players on the board
    def list_of_rk(self):
        return self.files['RK'].tolist()

    # returns the player name given a rank value
    def get_player_name_from_rank(self, rank):
        return self.files.loc[self.files['RK'] == rank, 'NAME'].iloc[0]


class Scores():
    '''A class that will utilize the player in Season stats and calculate the Fantasy Score'''

    score_dict = {"PTS": 1, "REB": 1.25, "AST": 1.5, "BLK": 2, "STL": 2,
                  "3PM": 0.5, "TO": -0.5, "DD2": 1.5, "TD3": 3}

    headers = ['RK', 'NAME', 'POS', 'PTS', 'REB', 'AST', 'BLK', 'STL', '3PM', 'TO', 'DD2', 'TD3']

    # we also take the DraftBoard as an input so that we can have access to the read dataframe
    # player row will be a row from the draftboard DF, essentially
    def __init__(self, files):
        self.files = files
        self.files = self.files.read_data()

    # the input is a players rank, and it will calculate the fantasy value, return a list with the player name
    # and the associated score
    def calculate_fantasy_score(self, rank):
        # isolate the df row, turn it into a lsit
        player_row = self.files[self.files.RK == rank]
        player_list = player_row.values.tolist()
        player_list.append(Scores.headers)

        # take that list and calculate the total fantasy score return the player name, position and total score
        fantasy_value = sum([player_list[0][i] * Scores.score_dict[player_list[1][i]]
                             for i in range(len(player_list[0])) if player_list[1][i] in Scores.score_dict.keys()])

        return [player_list[0][1], player_list[0][2], fantasy_value]


class Player():
    '''The class build a player dataframe. Essentially has all the methods that will store when a player when
    it is drafted and the stats with their respective dataframe'''

    # data files as input, as also initialize an empty df for the player
    def __init__(self, files):
        self.files = files
        self.files = self.files.read_data()

        # create a empty dataframe whil keeping the headers
        self.player_board = pd.DataFrame().reindex_like(self.files[:0])
        self.player_board['FANTASY_SCORE'] = np.nan

    # this method will append a player into the teams dataframe
    def draft_player(self, rank):
        self.player_board = self.player_board.append(self.files[self.files.RK == rank], sort=False)

    # this method inputs the output from Score.calculate_fantasy_score and adds that fantasy value into the
    # Fantasy_Score column
    def add_fantasy_score(self, fantasy_score):
        self.player_board.loc[self.player_board.NAME == fantasy_score[0], 'FANTASY_SCORE'] = fantasy_score[2]

    # this method sums the FANTASY_score column and returns the total value of the team's score
    def sum_fantasy(self):
        return self.player_board['FANTASY_SCORE'].sum()

    # this methods is used at the end of the game to return the players list of players draft
    # and their assoicted fantasy score
    def return_team(self):
        return self.player_board[['NAME', 'FANTASY_SCORE']]

    def __repr__(self):
        return repr(self.player_board)


class Engine():

    def __init__(self):
        self.files = Files('NBA_data.csv')
        self.board = DraftBoard(self.files)
        self.scores = Scores(self.files)

    # utilizies the above classes to start the draft
    def play_game(self):

        #explain the game
        print('Welcome to the most simple NBA mock draft you have ever played! This concept is based of of ESPN '
              'Fantasy and follows a snake draft format. You will get to select how many teams you want in the league '
              'with the caveat of a min of 5 and a max of 13 teams. The draft board consists of all the NBA players '
              'who have played in the 19-20 NBA Season, and are ordered by end of season ranking. '
              'You will see their raw score but not their fantasy value! When the computer '
              'autodrafts, they will select the first avaliable player on the board, you have the option to do this as well ')

        print('Each category represents a fantasy value: ')
        print('Points: +1')
        print('3 Point Shot: +0.5')
        print('Rebound: +1.25')
        print('Assist: +1.5')
        print('Steal: +2')
        print('Block: +2')
        print('Turnover: -0.5')
        print('DD: +1.5')
        print('TD: +3')


        # we first ask the user how many teams they want in the league
        # we use the while loop to error check for our team numbers, and the try except
        # to be rasied when they input sometihng other than an integer
        try:
            while True:
                team_num = int(input('Please enter how many teams you do want in the league?: '))
                if team_num >= 5 and team_num <= 13:
                    break
                else:
                    print('This league only allows a minimum of 5 and a maximum of 13 teams!!')
        except:
            raise TypeError("Only integers are allowed")

        # create a list of n players that is inputted by the user. Each list if a class Player that is created above
        player_list = [Player(self.files) for i in range(team_num)]

        # we are creating a list of lists, which each index as the round of the draft. The values inside are
        # the draft order for that round. We follow snake draft, so if its 1,2,3 first round, second round is 3,2,1
        first_round_order = list(range(1, team_num + 1))
        draft_order = [first_round_order[::-1] if i % 2 != 0 else first_round_order for i in range(1, 13)]
        draft_order.insert(0, first_round_order)

        # print the first round draft order, as well as the user's team number
        users_team_num = random.choice(draft_order[0])
        print(f'You are team {users_team_num}, please take note of your team number.')
        print(f'This is the first round draft order{draft_order[0]}')
        print('Since we are using a snake draft round 2 will be the reverse of round 1 and so on to round 13.')

        # ask user to start the game
        try:
            while True:
                start_game = int(input('Are you ready to start the game?: [1] Yes [2] No '))
                if start_game == 2:
                    print('You have decided not to begin the draft, the program will exit now')
                    return 'Good bye!'
                elif start_game == 1:
                    print('Draft is starting now, good luck!')
                    break
        except:
            raise TypeError("Only integers are allowed")

        # loop that runs through the entire list, which is all 13 rounds, and a inner loop that runs through
        # each draft selection. If the draft number == the players number, than they will get to select
        # who to choose, if its not =, than the computer will autodraft the first player on the board.
        draft_num = 1
        for h in range(len(draft_order)):

            # this variable is called in if else statements below to reverse the index when appending a drafted player
            # [i if h % 2 == 0 else rev_order - h] <- this code you will see here is changing the index
            # depending on what round of the draft we are on.
            rev_order = -1

            for i in range(len(draft_order[0])):
                if draft_order[h][i] != users_team_num:

                    # the computer will autoselect the first player on the draft board
                    # we then add that player to that Player objects list and calcualte it's fantasy score
                    print(f"In round {h + 1} of the draft, " \
                          f"team {draft_order[h][i]} has autodrafted {self.board.get_first_player_name()}, " \
                          f"who has a fantasy score of {self.scores.calculate_fantasy_score(self.board.get_rank_first_row())[-1]}")

                    player_list[i if h % 2 == 0 else rev_order - i].draft_player(self.board.get_rank_first_row())
                    player_list[i if h % 2 == 0 else rev_order - i].add_fantasy_score(
                        self.scores.calculate_fantasy_score(self.board.get_rank_first_row()))
                    self.board.draft_player(self.board.get_rank_first_row())

                # else is triggered when it is the user's turn to draft, we ask the user if he/she wants to
                # autodraft or sleect the player they want
                else:
                    try:
                        while True:
                            user_draft = int(input('It is your turn to draft! Please select an option'
                                                   ' [1] Select a player [2] Autodraft '))

                            # if user selects 2, we will just autodraft the first player on the board
                            if user_draft == 2:
                                print(f"In round {h + 1} of the draft, you have autodrafted " \
                                f"{self.board.get_first_player_name()}, who has a fantasy score of " \
                                f"{self.scores.calculate_fantasy_score(self.board.get_rank_first_row())[-1]}")

                                player_list[i if h % 2 == 0 else rev_order - i].draft_player(
                                    self.board.get_rank_first_row())
                                player_list[i if h % 2 == 0 else rev_order - i].add_fantasy_score(
                                    self.scores.calculate_fantasy_score(self.board.get_rank_first_row()))
                                self.board.draft_player(self.board.get_rank_first_row())

                                break
                            # this is the code where the user will select a player on the board
                            elif user_draft == 1:
                                self.board.show_board()

                                # error checking on user input for the player he/she wants to draft
                                # need to add error checking to only input rank that is on the board
                                try:
                                    while True:
                                        draft_rk = int(input('Please enter the rank of the player'
                                                             ' that you want to draft OR [0] to show more players: '))

                                        if draft_rk in self.board.list_of_rk():
                                            print(f"In round {h + 1} of the draft, " \
                                                  f"you have selected {self.board.get_player_name_from_rank(draft_rk)}, " \
                                                  f"who has a fantasy score of {self.scores.calculate_fantasy_score(draft_rk)[-1]}")

                                            player_list[i if h % 2 == 0 else rev_order - i].draft_player(draft_rk)
                                            player_list[i if h % 2 == 0 else rev_order - i].add_fantasy_score(
                                                self.scores.calculate_fantasy_score(draft_rk))
                                            self.board.draft_player(draft_rk)

                                            break

                                        # here we give the player an option to show more players on the draftboard
                                        # if they want to see more than 50 on the board
                                        elif draft_rk == 0:
                                            row_num = int(input('Please enter the number of rows'
                                                                ' that you want to display on the board, note the default is 50: '))
                                            self.board.show_board_input(row_num)

                                        else:
                                            print('You entered a player rank currently not on the board!!')
                                except:
                                    raise TypeError("Only integers are allowed")

                                break

                    except:
                        raise TypeError("Only integers are allowed")

                        # draft is complete let the player choose what he wants to see, his team, overall ranking, or exit
        try:
            while True:
                end_game = int(input('Congrats on finishing the draft!'
                                     'Please select [1] View teams [2] Draft Summary [3] Exit: '))

                # when the input = 3, we end the draft and the program closes
                if end_game == 3:
                    print('Thank you for drafting!')
                    return 'Good bye!'

                # when the input = 1, we ask the user which team number do they want didplay
                # as used previosuly the while loop keeps looking till the user inputs a valid number
                elif end_game == 1:

                    while True:
                        view_team = int(input('Please insert a team number to view their team:'))

                        if view_team in first_round_order:
                            print(player_list[view_team - 1].return_team())
                            break

                        else:
                            print('You selected a team that is not part of the draft!!!')
                            break

                # when the value = 2 we calculate the total fantasy score, and then print the final results
                # in desc order of first to last
                elif end_game == 2:
                    fantasy_final_sum_list = sorted([(player_list[i].sum_fantasy(), i + 1)
                                                     for i in range(len(player_list))], reverse=True)

                    # print final standings
                    for i in range(len(fantasy_final_sum_list)):
                        if fantasy_final_sum_list[i][1] == users_team_num:
                            print(f'Place: {i + 1} Team: YOU Score: {fantasy_final_sum_list[i][0]}')
                        else:
                            print(
                                f'Place: {i + 1} Team: {fantasy_final_sum_list[i][1]} Score: {fantasy_final_sum_list[i][ 0]}')

        except:
            raise TypeError("Only integers are allowed")


engine = Engine()
engine.play_game()