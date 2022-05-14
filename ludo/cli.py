from .game import Player, Game
from .painter import present_6_dice_name
from .recorder import RunRecord, MakeRecord
from os import linesep
from collections import deque


MASTER = 1
PRINT_TO_ALL = 0

class CLIGame():

    def __init__(self):
        self.prompt_end = "> "
        self.game = Game()
        # used for nicer printing
        self.prompted_for_pawn = False
        # saving game data
        self.record_maker = MakeRecord()
        # getting game data
        self.record_runner = None

    def myprint(self, players_IDs, msg):
        #for debug
        print(msg)
        msg = msg + "\n"
        if players_IDs == PRINT_TO_ALL:
            #send message to all connected players
            for player in self.game.players:
                if player.conn is not None:
                    player.conn.send(msg.encode())
        else:
            #send the msg to the players specified
            for player in self.game.players:
                if player.ID in players_IDs and player.conn is not None:
                    player.conn.send(msg.encode())
        return 

    def myinput(self, player_ID, msg):
        #get the input from corresponding player
        for player in self.game.players:
            if player.ID == player_ID: 
                break
        if msg is not None:
            print(msg)
            msg = msg + "\n"
            player.conn.send(msg.encode())
        msg = player.conn.recv(2048).decode()
        print("<player " + str(player.ID) + ">",msg)
        return msg

    def validate_input(self, player_input, players_output, prompt, desire_type, allawed_input=None,
                       error_mess="Invalid Option!", str_len=None):
        '''
        loop while receive correct value
        param allowed_input can be list of allowed values
        param str_len is two sized tuple if min and max
        '''
        prompt += linesep
        while True:
            choice = self.myinput(player_input, prompt)
            if not choice:
                self.myprint(players_output, linesep + error_mess)
                continue
            try:
                choice = desire_type(choice)
            except ValueError:
                self.myprint(players_output,linesep + error_mess)
                continue
            if allawed_input:
                if choice in allawed_input:
                    break
                else:
                    self.myprint(players_output,"Invalid Option!")
                    continue
            elif str_len:
                min_len, max_len = str_len
                if min_len < len(choice) < max_len:
                    break
                else:
                    self.myprint(players_output,linesep + error_mess)
            else:
                break
        self.myprint(players_output,'\n')
        return choice

    def get_user_initial_choice(self):
        text = linesep.join(["choose option",
                             "0 - start new game",
                             "1 - run (review) recorded game"])
        choice = self.validate_input(MASTER, [MASTER], text, int, (0, 1))
        return choice

    def prompt_for_file(self, mode="rb"):
        '''return file descriptor'''
        text = "Enter filename (name of the record)"
        while True:
            filename = self.validate_input(MASTER, [MASTER], text, str)
            try:
                file_descr = open(filename, mode=mode)
                return file_descr
            except IOError as e:
                print(e)
                print("Try again")

    def does_user_want_save_game(self):
        '''return True if user want to save
        game or False
        '''
        text = linesep.join(["Save game?",
                             "0 - No",
                             "1 - Yes"])
        choice = self.validate_input(MASTER, [MASTER], text, int, (0, 1))
        return choice 

    def choose_name(self, player):

        name = self.validate_input(player.ID, [player.ID],"Enter name for player", str, str_len=(1, 30))
        name = name[0:-1]
        player.name = name

    def master_prompt_for_player(self):
        ''' get player attributes from myinput,
        initial player instance and
        add player to the game
        '''
        
        #if choosing player options for Master (choose_pawn_delegate will be None when first entered in list)
        if self.game.players[0].choose_pawn_delegate == None:
            #for Master player, assume human and all colours
            available_colours = sorted(['yellow', 'blue', 'red', 'green'])
            name = self.validate_input(MASTER,[MASTER],"Enter name for player", str, str_len=(1, 30))
            name = name[0:-1]
            available_options = range(len(available_colours))
            options = ["{} - {}".format(index, colour)
                    for index, colour in
                    zip(available_options,
                    available_colours)]
            text = "choose colour" + linesep
            text += linesep.join(options)
            choice = self.validate_input(MASTER,[MASTER],text, int, available_options)
            colour = available_colours.pop(choice)

            player = Player(MASTER, colour, name, self.prompt_choose_pawn, self.master_conn)

            self.game.players = deque()
            self.game.add_player(player)
    
        #else choosing options for other human or pc players
        else:
            available_colours = self.game.get_available_colours()

            text = linesep.join(["choose type of player",
                                "0 - computer",
                                "1 - human"])
            choice = self.validate_input(MASTER, [MASTER], text, int, (0, 1))

            if choice == 1:
                available_options = range(len(available_colours))
                if len(available_options) > 1:
                    # show available colours
                    options = ["{} - {}".format(index, colour)
                            for index, colour in
                            zip(available_options,
                            available_colours)]
                    text = "choose colour" + linesep
                    text += linesep.join(options)
                    choice = self.validate_input(MASTER, [MASTER],text, int, available_options)
                    colour = available_colours.pop(choice)
                else:
                    # only one colour left
                    colour = available_colours.pop()
                name = "Player " + str(len(self.game.players)+1)
                player = Player(len(self.game.players)+1, colour, name, self.prompt_choose_pawn)
            elif choice == 0:
                # automatically assign colours
                colour = available_colours.pop()
                player = Player(len(self.game.players)+1, colour)
            self.game.add_player(player)

    def master_prompt_for_players(self):
        '''put all players in the game'''
        counts = ("first", "second", "third", "fourth last")
        text_add = "Add {} player"
        for i in range(2):
            if i == 0:
                self.myprint([MASTER],"Setting up your player (MASTER)")
            else:
                self.myprint([MASTER],text_add.format(counts[i]))
            self.master_prompt_for_player()
            self.myprint([MASTER],"Player added\n")

        text = linesep.join(["Choose option:",
                             "0 - add player",
                             "1 - start game with {} players"])
        for i in range(2, 4):
            choice = self.validate_input(MASTER, [MASTER], text.format(str(i)), int, (0, 1))
            if choice == 1:
                break
            elif choice == 0:
                self.myprint([MASTER], text_add.format(counts[i]))
                self.master_prompt_for_player()
                self.myprint([MASTER], "Player added\n")

    def prompt_choose_pawn(self):
        '''used when player (human) has more than
        one possible pawn to move.
        This method is pass as a callable during
        player instantiation
        '''
        text = present_6_dice_name(self.game.rolled_value,
                                  str(self.game.curr_player))
        text += linesep + "has more than one possible pawns to move."
        text += " Choose pawn" + linesep
        pawn_options = ["{} - {}".format(index + 1, pawn.id)
                        for index, pawn
                        in enumerate(self.game.allowed_pawns)]
        text += linesep.join(pawn_options)
        index = self.validate_input(self.game.curr_player.ID, [self.game.curr_player.ID],
            text, int, range(1, len(self.game.allowed_pawns) + 1))
        self.prompted_for_pawn = True
        return index - 1

    def prompt_to_continue(self, player_input_ID):
        for player in self.game.players:
            if player.ID == player_input_ID:
                break
        if player.conn is None:
            return
        else:
            text = "press Enter to continue" + linesep
            self.myinput(player_input_ID,text) 

    def print_players_info(self):
        word = "start" if self.game.rolled_value is None else "continue"
        self.myprint(PRINT_TO_ALL,"Game {} with {} players:".format(
              word,
              len(self.game.players)))
        for player in self.game.players:
            self.myprint(PRINT_TO_ALL,"{}({})".format(player.name, player.colour))
        self.myprint(PRINT_TO_ALL,'\n')

    def print_info_after_turn(self):
        '''it used game attributes to printing info'''
        pawns_id = [pawn.id for pawn in self.game.allowed_pawns]
        # nicer printing of dice
        message = present_6_dice_name(self.game.rolled_value,
                                     str(self.game.curr_player))
        message += linesep
        if self.game.allowed_pawns:
            message_moved = "{} is moved. ".format(
                self.game.picked_pawn.id)
            if self.prompted_for_pawn:
                self.prompted_for_pawn = False
                self.myprint(PRINT_TO_ALL,message_moved)
                return
            message += "{} possible pawns to move.".format(
                " ".join(pawns_id))
            message += " " + message_moved
            if self.game.jog_pawns:
                message += "Jog pawn "
                message += " ".join([pawn.id for pawn in self.game.jog_pawns])
        else:
            message += "No possible pawns to move."
        self.myprint(PRINT_TO_ALL,message)

    def print_standing(self):
        standing_list = ["{} - {}".format(index + 1, player)
                         for index, player in enumerate(self.game.standing)]
        message = "Standing:" + linesep + linesep.join(standing_list)
        self.myprint(PRINT_TO_ALL,message)

    def print_board(self):
        self.myprint(PRINT_TO_ALL,self.game.get_board_pic())

    def load_recorded_players(self):
        '''get recorded (save) players from
        recorder and put them in game
        '''
        if self.record_runner is None:
            file_descr = self.prompt_for_file()
            self.record_runner = RunRecord(file_descr)
            file_descr.close()
        for player in self.record_runner.get_players(
                self.prompt_choose_pawn):
            self.game.add_player(player)

    def run_recorded_game(self):
        '''get history of game (rolled_value
        and  index's allowed pawn) from 
        record_runner in order to replay game'''
        self.load_recorded_players()
        self.print_players_info()
        self.prompt_to_continue(MASTER)
        for rolled_value, index in self.record_runner:
            self.game.play_turn(index, rolled_value)
            self.print_info_after_turn()
            self.print_board()
            self.prompt_to_continue(MASTER)
            self.print_board()

    def record_players(self):
        '''save players on recorder'''
        for player in self.game.players:
            self.record_maker.add_player(player)

    def connect_player(self,player):
        Pass = 0
        #cicle for all players trying to connect
        while Pass != self.GamePass:
            player.conn, addr = self.server.accept()
            #3 chances per player to guess the Pass
            for i in range(3):
                prompt = "Game Password? (try " + str(i+1) + "/3)"
                Pass = self.validate_input(player.ID, [player.ID], prompt, str)
                if Pass == self.GamePass:
                    break
                else:
                    self.myprint([player.ID],"Wrong Password, try again")
            if Pass != self.GamePass:
                player.conn.close()
        self.choose_name(player)

        return

    def wait_for_connections(self):            
        #wait for other players to connect
        for player in self.game.players:
            #if player is human and not connected
            if player.choose_pawn_delegate is not None and player.conn is None:
                self.myprint(PRINT_TO_ALL,"waiting for player " + str(player.ID) + " to connect") 
                self.connect_player(player)
                self.myprint(PRINT_TO_ALL,"player " + str(player.ID) + " connected") 
        
        self.myprint(PRINT_TO_ALL, "all players connected") 

    def load_players_for_new_game(self):
        self.master_prompt_for_players()
        self.wait_for_connections()
        self.print_players_info()
        self.record_players()

    def play_game(self):
        '''mainly calling play_turn
        Game's method while game finished
        '''
        try:
            while not self.game.finished:
                self.game.play_turn()
                self.print_info_after_turn()
                self.print_board()
                self.record_maker.add_game_turn(
                    self.game.rolled_value, self.game.index)
                self.prompt_to_continue(self.game.curr_player.ID)
            self.myprint(PRINT_TO_ALL,"Game finished")
            self.print_standing()
            self.offer_save_game()
        except (KeyboardInterrupt, EOFError):
            print(linesep +
                  "Exiting game. ")
            raise

    def offer_save_game(self):
        '''offer user save game'''
        if self.does_user_want_save_game():
            file_descr = self.prompt_for_file(mode="wb")
            self.record_maker.save(file_descr)
            file_descr.close()
            print("Game is saved")
    
    def get_game_pass(self):
        prompt = "Set Game Pass for other human players to connect (4-30 char)"
        GamePass = self.validate_input(MASTER,[MASTER],prompt, str, str_len=(4, 30))
        return GamePass

    def start(self, master_conn, server):
        '''main method, starting cli'''
        self.master_conn = master_conn
        self.server = server
        master = Player(MASTER, "yellow", 'Master', None, master_conn)
        self.game.add_player(master)
        self.myprint(PRINT_TO_ALL,'\n')
        self.GamePass = self.get_game_pass()
        try:
            choice = self.get_user_initial_choice()
            if choice == 0:  # start new game
                self.load_players_for_new_game()
                self.play_game()
            elif choice == 1:  # review played game
                self.run_recorded_game()
        except (KeyboardInterrupt, EOFError):
            self.myprint(PRINT_TO_ALL,linesep + "Exit Game")


if __name__ == '__main__':
    CLIGame().start()
