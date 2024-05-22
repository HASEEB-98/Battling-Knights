import json

# global vairables:
surprise_attack_power = 0.5
item_priority = {'A': 3, 'M': 2, 'D': 1, 'H': 0}


class Knight:
    # initialisation of knight class
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos
        self.attack = 1
        self.defense = 1
        self.status = "LIVE"
        self.item = None
    
    # function to move knight
    def move(self, direction):
        if self.status != "LIVE":
            return
        
        x, y = self.position
        if direction == 'N':
            self.position = (x - 1, y)
        elif direction == 'E':
            self.position = (x, y + 1)
        elif direction == 'S':
            self.position = (x + 1, y)
        elif direction == 'W':
            self.position = (x, y - 1)
        
        # Check if moved out of bounds i.e knight is drowned
        if not (0 <= self.position[0] < 8) or not (0 <= self.position[1] < 8):
            
            print(f"{self.name} drowned!")
            self.knight_died('DROWNED')
        
         # update item position to knight position if knight owned any item
        elif self.item:
            self.item.position = self.position

    # equip any item if knight doesn't have any item, or current item priority is low
    def equip_item(self, item):
        # priority of each item
        if self.item is None or  item.priority > self.item.priority:
            # Un equip previous item
            if self.item:
                self.item.equiped_by = None
            
            self.item = item
            item.equiped_by = self.name

    # un equip item, if knight is drowned or dead
    def un_equip_item(self):
        if self.item:
            self.item.equiped_by = None
            self.item = None
            
    # this function acts as destructor whenever knight is drowned or dead
    # it will drop any item which knight owned, and reset the attack and defense power, furthermore if knight is drowned then it will also change position of knight to nukk
    def knight_died(self, status):
        self.status = status
        self.attack = 0
        self.defense = 0
        if status == 'DROWNED':
            self.position = None
        self.un_equip_item()

    # gives useful information regarding knight which is then used to store final state of board
    def get_info(self):
        return [
            list(self.position) if self.position else None,
            self.status,
            self.item.name if self.item else None,
            self.attack,
            self.defense
        ]

        


class Item:
    # initialisation of item class
    def __init__(self, name, start_pos, attack, defense, priority):
        self.name = name
        self.position = start_pos
        self.attack = attack
        self.defense = defense
        self.priority = priority
        self.equiped_by = None

    # gives useful information regarding item which is then used to store final state of board
    def get_info(self):
        return [list(self.position) if self.position else None, self.equiped_by]


# This function initialize the board with knights and items.
def initialize_board():
    items = {
        'A': Item('Axe', (2, 2), 2, 0, 3),
        'D': Item('Dagger', (2, 5), 1, 0, 1), 
        'M': Item('Helmet', (5, 2), 0, 1, 0), 
        'H': Item('MagicStaff', (5, 5), 1, 1, 2),
    }

    knights = {
        'R': Knight('RED', (0, 0)),
        'B': Knight('BLUE', (7, 0)),
        'G': Knight('GREEN', (7, 7)),
        'Y': Knight('YELLOW', (0, 7))
    }

    return items, knights

# Input validation function to make sure every move in move.txt file is a valid move
def are_moves_valid(moves):

    if not moves or moves[0] != "GAME-START" or moves[-1] != "GAME-END":
        print("Invalid moves file format.")
        return

    moves = moves[1:-1]

    possible_knight_keys = ['R', 'B', 'G', 'Y']
    possible_directions = ['N', 'E', 'S', 'W']

    for move in moves:
        knight_key, direction = move.split(':')
        if knight_key not in possible_knight_keys or direction not in possible_directions:
            return False

    return True     
    
# This function get moves from move.txt file and apply each move to respective knight mention in move
def process_moves(moves, items, knights):
    
    for move in moves:
        knight_key, direction = move.split(':')
        selected_knight = knights[knight_key]
        
        # Move the knight
        selected_knight.move(direction)
        
        # If knight is not ALIVE then we don't need to apply any processing
        if selected_knight.status != "LIVE":
            continue
        
        # Check if they land on an item
        pos = selected_knight.position
        for item_object in items.values():
            if selected_knight.position == item_object.position:
                selected_knight.equip_item(item_object)
        
        # Check for battles
        for other_knight in knights.values():
            if other_knight.name != selected_knight.name and selected_knight.position == other_knight.position:
                resolve_battle(selected_knight, other_knight)
                
        
# function to resolve battle between 2 knights, one of them is 
def resolve_battle(attacker, defender):
    # calculate full attack power of attacker including baas attack value of knight, item attack power, if any equiped by knight, and surprise attack power
    full_attack = attacker.attack + (attacker.item.attack if attacker.item else 0) + surprise_attack_power

    # calculate full defense power of defender including baas defense value of knight, item defesne power, if any equiped by knight
    full_defense = defender.defense + (defender.item.defense if defender.item else 0)

    # Attacker kills the defender knight is it has more attack power then defender defense power
    if full_attack > full_defense:
        print(f"{attacker.name} kills {defender.name}!")
        # Check if defender owned any item then propose this item to attacker
        if defender.item:
            attacker.equip_item(defender.item)
        defender.knight_died('DEAD')

    # Defender defends the attack and kills the attacker knight is it has more defense power then attacker
    else:
        print(f"{defender.name} defends successfully against {attacker.name}!")
        # Check if attacker owned any item then propose this item to defender
        if attacker.item:
            defender.equip_item(attacker.item)
        attacker.knight_died('DEAD')


# function to convert final state of the board to json file
def final_state_to_json(items, knights):
    state = {}
    for knight_object in knights.values():
        state[knight_object.name.lower()] = knight_object.get_info()

    for item_object in items.values():
        state[item_object.name] = item_object.get_info()
        
    return state

def main():
    # check if input file exists or not
    try:
        with open('moves.txt', 'r') as f:
            moves = f.read().splitlines()
    except FileNotFoundError:
        print("Error: The file 'moves.txt' does not exist.")
        return -1

    # input validation
    if not are_moves_valid(moves):
        print("Error: The file 'moves.txt' does not contain valid set of moves.")
        return -1
    
    moves = moves[1:-1]
    
    items, knights = initialize_board()

    print("Highlight in Knights Battle:\n")
    process_moves(moves, items, knights)

    final_state = final_state_to_json(items, knights)
    
    print("\nFinal results after the battle is stored in final_state.json file successfully!.")
    # store json to final_state.json file
    with open('final_state.json', 'w') as f:
        json.dump(final_state, f, indent=4)

if __name__ == "__main__":
    main()
