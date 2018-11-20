import random
import time

names = ['You', 'Steve', 'Geoff', 'Tim', 'Georg', 'Lucy', 'Timagain']
speed = 1.5


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
        print(self.players[lb_pos].name + ' is the small blind and bets ' + str(game.lb) + '. ' + self.players[
            bb_pos].name + ' is the big blind and bets ' + str(bb) + '.')
        self.bets[bb_pos] = bb
        self.bets[lb_pos] = self.lb
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
                    else:
                        time.sleep(speed)
                        print('Please choose from: check, call, raise , or fold.')
                new_player_index = self.active_players[(self.active_players.index(player_index) + 1) % len(self.active_players)]
                if folded == 1:
                    self.active_players.remove(player_index)
                player_index = new_player_index
                i += 1
        for player in self.players:
            player_index = player.position
            self.pot += self.bets[player_index]
            self.players[player_index].chips -= self.bets[player_index]
        time.sleep(speed)
        print('There are ' + str(self.pot) + ' chips in the pot.')

    def betting_round(self):
        self.bets = [0] * self.number_of_players
        bb = self.bb
        lb_pos = self.find_lb()
        while lb_pos not in self.active_players:
            lb_pos += 1
        time.sleep(speed)
        print(self.players[lb_pos].name + ' to bet first.')
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
                    else:
                        time.sleep(speed)
                        print('Please choose from: check, call, raise , or fold.')
                new_player_index = self.active_players[
                    (self.active_players.index(player_index) + 1) % len(self.active_players)]
                if folded == 1:
                    self.active_players.remove(player_index)
                player_index = new_player_index
                i += 1
        for player in self.players:
            player_index = player.position
            self.players[player_index].chips -= self.bets[player_index]
            self.pot += self.bets[player_index]

    def active_bets_equal(self):
        for i in self.active_players:
            if self.bets[i] != max(self.bets):
                return False
        return True

    def end_of_turn(self):
        if len(self.active_players) == 1:
            player_position = self.active_players[0]
        else:
            player_position = 0
        time.sleep(0.4)
        time.sleep(speed)
        print(self.players[player_position].name + ' won a pot of ' + str(self.pot) + ' chips.\n')
        self.round += 1
        self.used_cards = []
        bbpos = self.find_bb()
        for player in self.players:
            player.cards = []
            if player.position == player_position:
                player.chips += self.pot
            if player.BB == 1:
                player.LB = 1
                player.BB = 0
            elif player.LB == 1:
                    player.LB = 0
                    player.Dealer = 1
            elif player.Dealer == 1:
                    player.Dealer = 0
        bbpos = (bbpos + 1) % len(self.players)
        self.players[bbpos].set_bb()

        for player in self.players:
            if player.chips <= 0:
                self.remove_player(player.position)
                time.sleep(speed)
                print('Player ' + str(player.position) + ' has been knocked out!\n')
        if self.round % 5 == 0:
            self.raise_blinds()

    def hand_reader(self, hand):
        tc = self.table_cards
        if tc:
            cards = hand.append(tc)
            if self.pair_check(cards):
              print(self.pair(cards))
            elif self.high_card_check(cards):
              print(high_card(cards))
#            three_check(cards)
#            straight_check(cards)
#            flush_check(cards)
#            full_house_check(cards)
#            four_check(cards)
#            straight_flush_check(cards)
#            royal_flush_check(cards)

    def high_card_check(self, cards):
        return 1

    def high_card(self, cards):
      highest = 0
      high_card = ''
      for c in cards:
          if c.number > highest:
              highest = c.number
              high_card = c
      time.sleep(speed)
      return ('You have a ' + str(high_card.value) + ' high.')

    def pair_check(self, cards):
        for card1 in cards:
            for card2 in cards:
                if card1.isequal(card2) & card1.number == card2.number:
                  return 1
                

    def pair(self, cards):
        for card1 in cards:
            for card2 in cards:
                if card1.isequal(card2) & card1.number == card2.number:
                  time.sleep(speed)
                  return ('You have a pair of ' + str(card1.value))


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
        self.BB = 0
        self.LB = 0

    def set_bb(self):
        self.BB = 1
        self.Dealer = 0
        self.LB = 0

    def set_lb(self):
        self.LB = 1
        self.Dealer = 0
        self.BB = 0


class Card:
    def __init__(self, suit, value):
        self.value = value
        self.suit = suit
        self.number = 0
        if self.value == 'J':
            self.number = 11
        elif self.value == 'Q':
            self.number = 12
        elif self.value == 'K':
            self.number = 13
        elif self.value == 'A':
            self.number = 14
        else:
            self.number = int(self.value)

    def isequal(self, card2):
        if self.number == card2.number & self.suit == card2.suit:
            return 1
        else:
            return 0
            
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
            soot = 'Hearts'
        elif self.suit == 'C':
            soot = 'Clubs'
        elif self.suit == 'D':
            soot = 'Diamonds'
        else:
            soot = 'Spades'
        return str(val + ' of ' + soot)


no_of_players = 6
big_blind = 2
little_blind = 1
buy_in = 200


game = Game(no_of_players, big_blind, little_blind, 2, buy_in)


game.start_of_turn()
game.hand_reader(game.players[0].cards)
game.blind_betting_round()
if len(game.active_players) > 1:
    game.flop()
    game.betting_round()
if len(game.active_players) > 1:
    game.turn()
    game.betting_round()
if len(game.active_players) > 1:
    game.river()
    game.betting_round()
game.end_of_turn()
