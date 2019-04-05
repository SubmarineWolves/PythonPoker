import random
import time

#TODO - All-in bets, removing players and keeping the blind orders, fix the position/number issues with betting orders, split pots, heads up rounds.

names = ['You', 'Steve', 'Betsy', 'Tim', 'Georg', 'Lucy', 'Timagain']
speed = 0.5
turn_end_speed = 1.5
no_of_players = 6
big_blind = 2
little_blind = 1
buy_in = 6

class Game:
    def __init__(self, n, bb, lb, increment, start_chips):
        if n < 3:
            raise ValueError('Too few players to start game')
        else:
            self.active_players = list(range(n))
            self.pot = 0
            self.bets = [0] * n
            self.table_cards = []
            self.used_cards = []
            self.round = 0
            self.number_of_players = n
            self.bb = bb
            self.lb = lb
            self.increment = increment
            player_list = []
            for k in range(0, n):
                player = Player(start_chips, k, names[k])
                if k == 0:
                    player.Dealer = 1
                elif k == 2:
                    player.BB = 1
                elif k == 1:
                    player.LB = 1
                player_list.append(player)
            self.players = player_list

    def run(self):
      while len(self.players) > 2:
        self.start_of_turn()
        self.blind_betting_round()
        #Do a flop
        if len(self.active_players) > 1:
            self.flop()
            self.betting_round()
        #Do the turn
        if len(self.active_players) > 1:
            self.turn()
            print 'There is a ' + self.table_cards[0].show_card() + ', a ' + self.table_cards[1].show_card() + ', a ' + \
                  self.table_cards[2].show_card() + ', and a ' + self.table_cards[3].show_card() + ' on the table.'
            self.betting_round()
        #Do the river
        if len(self.active_players) > 1:
            self.river()
            print 'There is a ' + self.table_cards[0].show_card() + ', a ' + self.table_cards[1].show_card() + ', a ' + \
                  self.table_cards[2].show_card() + ', a ' + self.table_cards[3].show_card() + ', and a ' + self.table_cards[4].show_card() + ' on the table.'
            self.betting_round()
            print 'No more betting. On your backs:\n'
        #Chack everyone's hands and calculate the winner
        for i in range(len(self.active_players)):
            player_number = self.active_players[i]
            player = self.players[player_number]
            hand = player.cards
            card1 = player.cards[0].show_card()
            card2 = player.cards[1].show_card()
            name = str(player.name)
            if player.name == 'You':
                print 'You reveal your hand of ' + card1 + ' and ' + card2 + '.'
            else:
                print name + ' reveals their hand of ' + card1 + ' and ' + card2 + '.'
            time.sleep(speed)
            self.hand_reader(i)
            time.sleep(speed)
        #Give the winner the chips, and rejig the blinds
        self.end_of_turn()
        #If you are knocked out, the game ends
        if self.players[0].name != 'You':
          print "You lose!"
          return
        print 'Next round begins in:'
        time.sleep(turn_end_speed)
        print '3'
        time.sleep(turn_end_speed)
        print '2'
        time.sleep(turn_end_speed)
        print '1'
        time.sleep(turn_end_speed)

    def find_lb(self):
        for player in self.players:
            if player.LB == 1:
                return player.position

    def find_bb(self):
        for player in self.players:
            if player.BB == 1:
                return player.position

    def find_dealer(self):
        for player in self.players:
            if player.Dealer == 1:
                return player.position

    def find_lb_name(self):
        for player in self.players:
            if player.LB == 1:
                return player.name

    def find_bb_name(self):
        for player in self.players:
            if player.BB == 1:
                return player.name

    def find_dealer_name(self):
        for player in self.players:
            if player.Dealer == 1:
                return player.name

    def display_used_cards(self):
        for card in self.used_cards:
            print(card.value + card.suit)

    def raise_blinds(self):
        self.lb = self.bb
        self.bb = self.bb*self.increment

    def remove_player(self, j):
        new_players = []
        for player in self.players:
            if player.position != j:
                new_players.append(player)
        self.players = new_players

    def random_card(self):
        suits = ['H', 'C', 'D', 'S']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        while 0 == 0:
            suitint = random.randint(0, 3)
            valueint = random.randint(0, 12)
            suit = suits[suitint]
            value = values[valueint]
            card = Card(suit, value)
            card_used = 0
            for used_card in self.used_cards:
                if (card.suit == used_card.suit) and (card.value == used_card.value):
                    card_used = 1
            if card_used == 0:
                self.used_cards.append(card)
                return card

    def start_of_turn(self):
        self.bets = [0] * len(self.players)
        self.active_players = range(len(self.players))
        self.pot = 0

        for player in self.players:
            card_one = game.random_card()
            player.cards.append(card_one)
            card_two = game.random_card()
            player.cards.append(card_two)
        if self.players[0].Dealer:
            time.sleep(speed)
            print('\nYou are the dealer, blinds are: ' + str(game.lb) + ' and ' + str(game.bb) + '.')
        elif self.players[0].BB == 1:
            time.sleep(speed)
            print('\nYou are the big blind. You have automatically bet ' + str(game.bb) + '.')
        elif self.players[0].LB == 1:
            time.sleep(speed)
            print('\nYou are the little blind. You have automatically bet ' + str(game.lb) + '.')
        else:
            time.sleep(speed)
            print('\nBlinds are: ' + str(game.lb) + ' and ' + str(game.bb) + '.')
        time.sleep(speed)
        print('Your cards are: ' + self.players[0].cards[0].show_card() + ' and ' +
              self.players[0].cards[1].show_card())
        time.sleep(speed)
        print('You have ' + str(self.players[0].chips) + ' chips')

    def flop(self):
        card_one = self.random_card()
        card_two = self.random_card()
        card_three = self.random_card()
        time.sleep(speed)
        print('\nThe dealer deals a ' + card_one.show_card() + ', a ' + card_two.show_card() + ' and a ' +
              card_three.show_card() + ' to the table.')
        self.table_cards = [card_one, card_two, card_three]

    def turn(self):
        card_four = self.random_card()
        time.sleep(speed)
        print('\nThe dealer deals a ' + card_four.show_card() + ' to the table.')
        self.table_cards.append(card_four)

    def river(self):
        card_five = self.random_card()
        time.sleep(speed)
        print('\nThe river is a ' + card_five.show_card() + '. There will be no more cards dealt.')
        self.table_cards.append(card_five)

    def blind_betting_round(self):
        self.bets = [0] * self.number_of_players
        bb = self.bb
        bb_pos = self.find_bb()
        lb_pos = self.find_lb()
        time.sleep(speed)
        print(self.find_lb_name() + ' is the small blind and bets ' + str(game.lb) + '. ' + self.find_bb_name() + ' is the big blind and bets ' + str(bb) + '.')
        self.bets[lb_pos] = self.lb
        self.bets[bb_pos] = bb
        i = 0
        player_index = (bb_pos+1) % len(self.players)
        iterations = len(self.active_players)
        while i < iterations or not self.active_bets_equal():
            player = self.players[player_index]
            folded = 0
            if player_index != 0:
                to_call = max(self.bets)
                r = random.randint(0, 5)
                if r not in [0, 1]:
                    # call
                    if self.bets[player_index] == to_call:
                        time.sleep(speed)
                        print(player.name + ' checks.')
                    else:
                        self.bets[player_index] = to_call
                        time.sleep(speed)
                        print(player.name + ' calls ' + str(to_call) + '.')
                elif r == 1:
                    # raise
                    self.bets[player_index] = to_call + bb
                    time.sleep(speed)
                    print(player.name + ' raises to ' + str(to_call + bb) + '.')
                else:
                    # fold
                    if to_call != self.bets[player_index]:
                        folded = 1
                        time.sleep(speed)
                        print(player.name + ' folds.')
                    else:
                        time.sleep(speed)
                        print(player.name + ' checks.')
                i += 1
                new_player_index = self.active_players[(self.active_players.index(player_index) + 1) % len(self.active_players)]
                if folded == 1:
                    self.active_players.remove(player_index)
                player_index = new_player_index
            else:
                to_call = max(self.bets)
                user_acted = 0
                while user_acted == 0:
                    time.sleep(speed)
                    action = raw_input('What would you like to do?\n')
                    if action == 'check':
                        if max(self.bets) == 0:
                            user_acted = 1
                        else:
                            time.sleep(speed)
                            print('You can\'t check when there is already a non-zero bet on the table.')
                    elif action == 'call':
                        self.bets[0] = to_call
                        user_acted = 1
                        time.sleep(speed)
                        print('You bet ' + str(to_call) + ' chips.')
                    elif action == 'raise':
                        self.bets[0] = to_call + bb
                        user_acted = 1
                        time.sleep(speed)
                        print('You raise the bet to ' + str(to_call + bb))
                    elif action == 'fold':
                        folded = 1
                        user_acted = 1
                    elif action == 'info':
                        print('Your cards are: ' + self.players[0].cards[0].show_card() + ' and ' + self.players[0].cards[1].show_card())
                        self.hand_reader(0)
                    else:
                        time.sleep(speed)
                        print('Please choose from: check, call, raise, fold, or info.')
                new_player_index = self.active_players[(self.active_players.index(player_index) + 1) % len(self.active_players)]
                if folded == 1:
                    self.active_players.remove(player_index)
                player_index = new_player_index
                i += 1
        for player in self.players:
            player_index = player.position
            self.pot += self.bets[player_index]
            for player in self.players:
              if player.position == player_index:
                player.chips -= self.bets[player_index]
        time.sleep(speed)
        print('There are ' + str(self.pot) + ' chips in the pot.')

    def betting_round(self):
        self.bets = [0] * self.number_of_players
        bb = self.bb
        lb_pos = self.find_lb()
        while lb_pos not in self.active_players:
            lb_pos = (lb_pos + 1) % len(self.active_players)
        time.sleep(speed)
        print(self.find_lb_name() + ' to bet first.')
        i = 0
        player_index = lb_pos
        iterations = len(self.active_players)
        while i < iterations or not self.active_bets_equal():
            player = self.players[player_index]
            folded = 0
            if player_index != 0:
                to_call = max(self.bets)
                r = random.randint(0, 4)
                if r not in [0, 1]:
                    # call
                    if self.bets[player_index] == to_call:
                        time.sleep(speed)
                        print(player.name + ' checks.')
                    else:
                        self.bets[player_index] = to_call
                        time.sleep(speed)
                        print(player.name + ' calls ' + str(to_call) + '.')
                elif r == 1:
                    # raise
                    self.bets[player_index] = to_call + bb
                    time.sleep(speed)
                    print(player.name + ' raises to ' + str(to_call + bb) + '.')
                else:
                    # fold
                    if to_call != self.bets[player_index]:
                        folded = 1
                        time.sleep(speed)
                        print(player.name + ' folds.')
                    else:
                        time.sleep(speed)
                        print(player.name + ' checks.')
                i += 1
                new_player_index = self.active_players[
                    (self.active_players.index(player_index) + 1) % len(self.active_players)]
                if folded == 1:
                    self.active_players.remove(player_index)
                player_index = new_player_index
            else:
                to_call = max(self.bets)
                user_acted = 0
                while user_acted == 0:
                    time.sleep(speed)
                    action = raw_input('What would you like to do?\n')
                    if action == 'check':
                        if max(self.bets) == 0:
                            user_acted = 1
                        else:
                            time.sleep(speed)
                            print('You can\'t check when there is already a non-zero bet on the table.')
                    elif action == 'call':
                        self.bets[0] = to_call
                        user_acted = 1
                        time.sleep(speed)
                        print('You bet ' + str(to_call) + ' chips.')
                    elif action == 'raise':
                        self.bets[0] = to_call + bb
                        user_acted = 1
                        time.sleep(speed)
                        print('You raise the bet to ' + str(to_call + bb))
                    elif action == 'fold':
                        folded = 1
                        user_acted = 1
                    elif action == 'info':
                      print('Your cards are: ' + self.players[0].cards[0].show_card() + ' and ' + self.players[0].cards[1].show_card())
                      self.hand_reader(0)
                    else:
                        time.sleep(speed)
                        print('Please choose from: check, call, raise, fold, or info.')
                new_player_index = self.active_players[
                    (self.active_players.index(player_index) + 1) % len(self.active_players)]
                if folded == 1:
                    self.active_players.remove(player_index)
                player_index = new_player_index
                i += 1
        for player in self.players:
            player_index = player.position
            for player in self.players:
              if player.position == player_index:
                player.chips -= self.bets[player_index]
            self.pot += self.bets[player_index]

    def active_bets_equal(self):
        for i in self.active_players:
            if self.bets[i] != max(self.bets):
                return False
        return True

    def end_of_turn(self):
        max_score = 0
        for j in range(len(self.active_players)):
            max_score = max(max_score, self.hand_score(j))
        for j in range(len(self.active_players)):
            if max_score == self.hand_score(j):
                winner = self.active_players[j]
        time.sleep(speed)
        print(self.players[winner].name + ' won a pot of ' + str(self.pot) + ' chips.\n')
        self.round += 1
        self.used_cards = []
        #find blinds and dealer position
        bbpos = self.find_bb()
        lbpos = self.find_lb()
        dealpos = self.find_dealer()
        #unset all blind and dealer status
        for player in self.players:
            player.unset_bb()
            player.unset_lb()
            player.unset_dealer()
        #increment blind and dealer positions by 1 (mod no of players)
        bbpos = (bbpos + 1) % no_of_players
        lbpos = (lbpos + 1) % no_of_players
        dealpos = (dealpos + 1) % no_of_players
				#remember the winner
        winpos = self.players[winner].position
        #Then, for every player
        for player in self.players:
            #Everyone puts their cards back
            player.cards = []
            #Winner gets the cash
            if player.position == winpos:
                player.chips += self.pot
#############If that player is out, remove them#################
            if player.chips <= 0:
              self.remove_player(player.position)
              time.sleep(speed)
              if player.position == 0:
                print('You have been knocked out!\n')
              else:
                print(str(player.name) + '(' + str(player.position) + ') has been knocked out!\n')

        #Collect a list of player positions still in the game
        pnums = [0]
        for player in self.players:
            pnums.append(player.position)
						
				#Increment the blinds or dealer positions if they were knocked out
        while bbpos not in pnums:
						bbpos = (bbpos + 1) % no_of_players
        while lbpos not in pnums:
						lbpos = (lbpos + 1) % no_of_players
        while dealpos not in pnums:
						dealpos = (dealpos + 1) % no_of_players
				#Then set the blinds and dealer positions accordingly
        for player in self.players:
					if player.position == bbpos:
						player.set_bb()
					if player.position == lbpos:
						player.set_lb()
					if player.position == dealpos:
						player.set_dealer()
        #Raise blinds every 5 rounds
        if self.round % 5 == 0:
            self.raise_blinds()
        print 'The new big blind is ' + self.find_bb_name()
        print 'The new little blind is ' + self.find_lb_name()
        print 'The new dealer is ' + self.find_dealer_name()

    def hand_reader(self, n):
        player_number = self.active_players[n]
        hand = self.players[player_number].cards
        tc = self.table_cards
        if tc:
            cards = hand+tc
        else: cards = hand

        if self.royal_flush_check(cards):
            string = self.royal_flush(cards)
        elif self.straight_flush_check(cards):
            string = self.straight_flush(cards)
        elif self.four_check(cards):
            string = self.four(cards)
        elif self.full_house_check(cards):
            string = self.full_house(cards)
        elif self.flush_check(cards):
            string = self.flush(cards)
        elif self.straight_check(cards):
            string = self.straight(cards)
        elif self.three_check(cards):
            string = self.three(cards)
        elif self.two_pair_check(cards):
            string = self.two_pair(cards)
        elif self.pair_check(cards):
            string = self.pair(cards)
        else:
            string = self.high_card(cards)

        if self.players[player_number].name == 'You':
            print 'You have' + string
        else:
            print self.players[player_number].name + ' has' + str(string)

    def high_card(self, cards):
      highest = 0
      high_card = ''
      for c in cards:
          if c.number > highest:
              highest = c.number
              high_card = c
      time.sleep(speed)
      return ' a high card ' + str(high_card.word_value) + '.'

    def high_card_score(self, cards):
        highest = 0
        high_card = ''
        for c in cards:
            if c.number > highest:
                highest = c.number
                high_card = c
        return 0.01 * high_card.number

    def pair_check(self, cards):
        for card1 in cards:
            for card2 in cards:
                if (card1.number == card2.number) and (not card1.isequal(card2)):
                  return 1

    def pair(self, cards):
        for card1 in cards:
            for card2 in cards:
                if (card1.number == card2.number) and (not card1.isequal(card2)):
                  return ' a pair of ' + str(card1.word_value) + 's'

    def pair_score(self, cards):
        for card1 in cards:
            for card2 in cards:
                if (card1.number == card2.number) and (not card1.isequal(card2)):
                  return card1.number * 0.01

    def two_pair_check(self, cards):
        if len(cards) < 4:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    if not card2.isequal(card1):
                        for card3 in cards:
                            if card3.is_not_in_list([card1, card2]):
                                for card4 in cards:
                                    if card4.is_not_in_list([card1, card2, card3]):
                                        if card1.number == card2.number and card3.number == card4.number:
                                            return 1

    def two_pair(self, cards):
        for card1 in cards:
            for card2 in cards:
                if not card2.isequal(card1):
                    for card3 in cards:
                        if card3.is_not_in_list([card1, card2]):
                            for card4 in cards:
                                if card4.is_not_in_list([card1, card2, card3]):
                                    if len(cards)>=6:
                                        for card5 in cards:
                                            if card5.is_not_in_list([card1, card2, card3, card4]):
                                                for card6 in cards:
                                                    if card6.is_not_in_list([card1, card2, card3, card4, card5]):
                                                        if card1.number == card2.number and card3.number == card4.number and card5.number == card6.number:
                                                            if card1.number == min(card1.number, card5.number, card3.number):
                                                                return ' two pair with ' + str(card5.word_value) + 's and ' + str(card3.word_value) + 's'
                                                            elif card3.number == min(card1.number, card3.number, card5.number):
                                                                return ' two pair with ' + str(card1.word_value) + 's and ' + str(card5.word_value) + 's'
                                                            else: return ' two pair with ' + str(card1.word_value) + 's and ' + str(card3.word_value) + 's'
                                                        elif card1.number == card2.number and card3.number == card4.number:
                                                            return ' two pair with ' + str(
                                                                card1.word_value) + 's and ' + str(
                                                                card3.word_value) + 's'
                                    elif card1.number == card2.number and card3.number == card4.number:
                                        return ' two pair with ' + str(card1.word_value) + 's and ' + str(card3.word_value) + 's'
        return ' created an error, you bitch.'

    def two_pair_score(self, cards):
        for card1 in cards:
            for card2 in cards:
                if not card2.isequal(card1):
                    for card3 in cards:
                        if card3.is_not_in_list([card1, card2]):
                            for card4 in cards:
                                if card4.is_not_in_list([card1, card2, card3]):
                                    if len(cards)>=6:
                                        for card5 in cards:
                                            if card5.is_not_in_list([card1, card2, card3, card4]):
                                                for card6 in cards:
                                                    if card6.is_not_in_list([card1, card2, card3, card4, card5]):
                                                        if card1.number == card2.number and card3.number == card4.number and card5.number == card6.number:
                                                            if card1.number == min(card1.number, card5.number, card3.number):
                                                                if card5.number < card3.number:
                                                                    return int(card3.number) * 0.01 + int(card5.number) * 0.0001
                                                                else:
                                                                    return int(card5.number) * 0.01 + int(card3.number) * 0.0001
                                                            elif card3.number == min(card1.number, card3.number, card5.number):
                                                                if card5.number < card1.number:
                                                                    return int(card1.number) * 0.01 + int(card5.number) * 0.0001
                                                                else:
                                                                    return int(card5.number) * 0.01 + int(card1.number) * 0.0001
                                                            else:
                                                                if card1.number < card3.number:
                                                                    return int(card3.number) * 0.01 + int(card1.number) * 0.0001
                                                                else: return int(card1.number) * 0.01 + int(card3.number) * 0.0001
                                                        elif card1.number == card2.number and card3.number == card4.number:
                                                            if card1.number < card3.number:
                                                                return int(card3.number) * 0.01 + int(
                                                                    card1.number) * 0.0001
                                                            else:
                                                                return int(card1.number) * 0.01 + int(
                                                                    card3.number) * 0.0001
                                    elif card1.number == card2.number and card3.number == card4.number:
                                        if card1.number < card3.number:
                                            return int(card3.number) * 0.01 + int(card1.number) * 0.0001
                                        else: return int(card1.number) * 0.01 + int(card3.number) * 0.0001
        return 0

    def three_check(self, cards):
        if len(cards)<3:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    for card3 in cards:
                        if  card1.number == card2.number == card3.number and (not card1.isequal(card2)) and (
                                not card1.isequal(card3)) and (not card3.isequal(card2)):
                            return 1

    def three(self, cards):
        if len(cards)<3:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    for card3 in cards:
                        if  card1.number == card2.number == card3.number and (not card1.isequal(card2)) and (
                                not card1.isequal(card3)) and (not card3.isequal(card2)):
                            time.sleep(speed)
                            return ' three of a kind with ' + str(card1.word_value) + 's'

    def straight_check(self, cards):
        if len(cards)<5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    for card3 in cards:
                        for card4 in cards:
                            for card5 in cards:
                                if (card1.number == card2.number + 1) and (card2.number == card3.number + 1) and (
                                        card3.number == card4.number + 1) and (card4.number == card5.number + 1):
                                    return 1

    def straight(self, cards):
        for card1 in cards:
            for card2 in cards:
                for card3 in cards:
                    for card4 in cards:
                        for card5 in cards:
                            if (card1.number == card2.number + 1) and (card2.number == card3.number + 1) and (
                                    card3.number == card4.number + 1) and (card4.number == card5.number + 1):
                                high = max(card1.number, card2.number, card3.number, card4.number, card5.number)
                                if high == 11:
                                    high = ' Jack'
                                elif high == 12:
                                    high = ' Queen'
                                elif high == 13:
                                    high = ' King'
                                elif high == 14:
                                    high = 'n Ace'
                                else: high = ' ' + str(high)
                                return ' a' + high + ' high straight.'

    def flush_check(self, cards):
        if len(cards) < 5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    if not card2.isequal(card1):
                        for card3 in cards:
                            if (not card3.isequal(card2)) and (not card3.isequal(card1)):
                                for card4 in cards:
                                    if (not card4.isequal(card3)) and (not card4.isequal(card2)) and \
                                            (not card4.isequal(card1)):
                                        for card5 in cards:
                                            if card1.suit == card2.suit == card3.suit == card4.suit == card5.suit and (
                                                    not card5.isequal(card4)) and (not card5.isequal(card3)) and \
                                                    (not card5.isequal(card2)) and (not card5.isequal(card1)):
                                                return 1

    def flush(self, cards):
        if len(cards) < 5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    if not card2.isequal(card1):
                        for card3 in cards:
                            if (not card3.isequal(card2)) and (not card3.isequal(card1)):
                                for card4 in cards:
                                    if (not card4.isequal(card3)) and (not card4.isequal(card2)) and \
                                            (not card4.isequal(card1)):
                                        for card5 in cards:
                                            if card1.suit == card2.suit == card3.suit == card4.suit == card5.suit and (
                                                    not card5.isequal(card4)) and (not card5.isequal(card3)) and \
                                                    (not card5.isequal(card2)) and (not card5.isequal(card1)):
                                                soot = card1.suit
                                                if soot == 'H':
                                                    sooot = 'heart'
                                                elif soot == 'S':
                                                    sooot = 'spade'
                                                elif soot == 'D':
                                                    sooot = 'diamond'
                                                else: sooot = 'club'
                                                return ' a ' + sooot + ' flush.'

    def full_house_check(self, cards):
        if len(cards) < 5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    if not card2.isequal(card1):
                        for card3 in cards:
                            if (not card3.isequal(card2)) and (not card3.isequal(card1)):
                                for card4 in cards:
                                    if (not card4.isequal(card3)) and (not card4.isequal(card2)) and \
                                            (not card4.isequal(card1)):
                                        for card5 in cards:
                                            if card1.number == card2.number and card3.number == card4.number == card5.number and (
                                                    not card5.isequal(card4)) and (not card5.isequal(card3)) and \
                                                    (not card5.isequal(card2)) and (not card5.isequal(card1)):
                                                return 1

    def full_house(self, cards):
        if len(cards) < 5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    if not card2.isequal(card1):
                        for card3 in cards:
                            if (not card3.isequal(card2)) and (not card3.isequal(card1)):
                                for card4 in cards:
                                    if (not card4.isequal(card3)) and (not card4.isequal(card2)) and \
                                            (not card4.isequal(card1)):
                                        for card5 in cards:
                                            if card1.number == card2.number and card3.number == card4.number == card5.number and (
                                                    not card5.isequal(card4)) and (not card5.isequal(card3)) and \
                                                    (not card5.isequal(card2)) and (not card5.isequal(card1)):
                                                return ' a full house with ' + card3.word_value + 's over ' + card1.word_value + 's'

    def four_check(self, cards):
        if len(cards) < 4:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    if not card2.isequal(card1):
                        for card3 in cards:
                            if (not card3.isequal(card2)) and (not card3.isequal(card1)):
                                for card4 in cards:
                                    if (not card4.isequal(card3)) and (not card4.isequal(card2)) and \
                                            (not card4.isequal(card1)):
                                        if card1.number == card2.number == card3.number == card4.number:
                                            return 1

    def four(self, cards):
        for card1 in cards:
            for card2 in cards:
                if not card2.isequal(card1):
                    for card3 in cards:
                        if (not card3.isequal(card2)) and (not card3.isequal(card1)):
                            for card4 in cards:
                                if (not card4.isequal(card3)) and (not card4.isequal(card2)) and \
                                        (not card4.isequal(card1)):
                                    if card1.number == card2.number == card3.number == card4.number:
                                        return ' four of a kind with ' + card1.word_value + 's'

    def straight_flush_check(self, cards):
        if len(cards) < 5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    for card3 in cards:
                        for card4 in cards:
                            for card5 in cards:
                                if (card1.number == card2.number + 1) and (card2.number == card3.number + 1) and (
                                        card3.number == card4.number + 1) and (card4.number == card5.number + 1):
                                    if card1.suit == card2.suit == card3.suit == card4.suit:
                                        return 1

    def straight_flush(self, cards):
        for card1 in cards:
            for card2 in cards:
                for card3 in cards:
                    for card4 in cards:
                        for card5 in cards:
                            if (card1.number == card2.number + 1) and (card2.number == card3.number + 1) and (
                                    card3.number == card4.number + 1) and (card4.number == card5.number + 1) and \
                                    (card1.suit == card2.suit == card3.suit == card4.suit):
                                high = max(card1.number, card2.number, card3.number, card4.number, card5.number)
                                if high == 11:
                                    high = 'Jack'
                                elif high == 12:
                                    high = 'Queen'
                                elif high == 13:
                                    high = 'King'
                                return ' a ' + high + ' high straight flush.'

    def royal_flush_check(self, cards):
        if len(cards) < 5:
            return 0
        else:
            for card1 in cards:
                for card2 in cards:
                    for card3 in cards:
                        for card4 in cards:
                            for card5 in cards:
                                if (card1.number == card2.number + 1) and (card2.number == card3.number + 1) and (
                                        card3.number == card4.number + 1) and (card4.number == card5.number + 1):
                                    if card1.suit == card2.suit == card3.suit == card4.suit and (
                                        14 == max(card1.number, card2.number, card3.number, card4.number, card5.number)):
                                        return 1

    def royal_flush(self, cards):
        for card1 in cards:
            for card2 in cards:
                for card3 in cards:
                    for card4 in cards:
                        for card5 in cards:
                            if (card1.number == card2.number + 1) and (card2.number == card3.number + 1) and (
                                    card3.number == card4.number + 1) and (card4.number == card5.number + 1) and \
                                    (card1.suit == card2.suit == card3.suit == card4.suit):
                                return ' a royal flush of ' + card1.suit + '.'

    def hand_score(self, n):
        player_number = self.active_players[n]
        hand = self.players[player_number].cards
        tc = self.table_cards
        if tc:
            cards = hand + tc
        else:
            cards = hand
        if self.royal_flush_check(cards):
            score = 9
        elif self.straight_flush_check(cards):
            score = 8
        elif self.four_check(cards):
            score = 7
        elif self.full_house_check(cards):
            score = 6
        elif self.flush_check(cards):
            score = 5
        elif self.straight_check(cards):
            score = 4
        elif self.three_check(cards):
            score = 3
        elif self.two_pair_check(cards):
            score = 2 + self.two_pair_score(cards)
        elif self.pair_check(cards):
            score = 1 + self.pair_score(cards)
        else: score = self.high_card_score(cards)
        return score

class Player:
    def __init__(self, chips, pos, name):
        self.name = name
        self.chips = chips
        self.cards = []
        self.BB = 0
        self.LB = 0
        self.Dealer = 0
        self.position = pos
        if pos == 0:
            self.Dealer = 1
        elif pos == 1:
            self.LB = 1
        elif pos == 2:
            self.BB = 1

    def set_dealer(self):
        self.Dealer = 1

    def set_bb(self):
        self.BB = 1

    def set_lb(self):
        self.LB = 1

    def unset_dealer(self):
        self.Dealer = 0

    def unset_bb(self):
        self.BB = 0

    def unset_lb(self):
        self.LB = 0    

class Card:
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit
        self.number = 0
        if self.value == 'J':
            self.number = 11
            self.word_value = 'Jack'
        elif self.value == 'Q':
            self.number = 12
            self.word_value = 'Queen'
        elif self.value == 'K':
            self.number = 13
            self.word_value = 'King'
        elif self.value == 'A':
            self.number = 14
            self.word_value = 'Ace'
        else:
            self.number = int(self.value)
            self.word_value = str(self.number)

    def isequal(self, equalcard):
        if (self.number == equalcard.number) & (self.suit == equalcard.suit):
            return 1
        else:
            return 0

    def is_not_in_list(self, cards):
        for card in cards:
            if self.isequal(card):
                return 0
        return 1
            
    def show_card(self):
        if self.value == 'J':
            val = 'Jack'
        elif self.value == 'Q':
            val = 'Queen'
        elif self.value == 'K':
            val = 'King'
        elif self.value == 'A':
            val = 'Ace'
        else:
            val = self.value
        if self.suit == 'H':
            soot = 'hearts'
        elif self.suit == 'C':
            soot = 'clubs'
        elif self.suit == 'D':
            soot = 'diamonds'
        else:
            soot = 'spades'
        return val + ' of ' + soot

game = Game(no_of_players, big_blind, little_blind, 2, buy_in)

game.run()