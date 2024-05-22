import json

surprise_attack_power = 0.5

class Knight:
    def __init__(self, name, start_pos):
        self.name = name
        self.position = start_pos
        self.attack = 1
        self.defense = 1
        self.status = "LIVE"
        self.item = None
    
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
        
        # Check if moved out of bounds
        if not (0 <= self.position[0] < 8) or not (0 <= self.position[1] < 8):
            
            print(f"{self.name} drowned!")
            self.knight_died('DROWNED')
        
        elif self.item:
            self.item.position = self.position

    def equip_item(self, item):
        item_priority = {'A': 3, 'M': 2, 'D': 1, 'H': 0}
        if self.item is None or  item.priority > self.item.priority:
            self.item = item
            item.equiped_by = self

    def un_equip_item(self):
        if self.item:
            self.item.equiped_by = None
            self.item = None
            

    def knight_died(self, status):
        self.status = status
        self.attack = 0
        self.defense = 0
        if status == 'DROWNED':
            self.position = None
        self.un_equip_item()

    def get_info(self):
        return [
            list(self.position) if self.position else None,
            self.status,
            self.item.name if self.item else None,
            self.attack,
            self.defense
        ]

    def __str__(self):
        item_name = self.item.name if self.item else "None"
        position = self.position if self.position else "None"
        



class Item:
    def __init__(self, name, start_pos, attack, defense, priority):
        self.name = name
        self.position = start_pos
        self.attack = attack
        self.defense = defense
        self.priority = priority
        self.equiped_by = None

    def get_info(self):
        return [list(self.position) if self.position else None, self.equiped_by]


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
    

def process_moves(moves, items, knights):
    
    for move in moves:
        knight_key, direction = move.split(':')
        selected_knight = knights[knight_key]
        
        # Move the knight
        selected_knight.move(direction)
        
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
                
        

def resolve_battle(attacker, defender):
    full_attack = attacker.attack + (attacker.item.attack if attacker.item else 0) + surprise_attack_power
    full_defense = defender.defense + (defender.item.defense if defender.item else 0)

    if full_attack > full_defense:
        print(f"{attacker.name} kills {defender.name}!")
        if defender.item:
            attacker.equip_item(defender.item)
        defender.knight_died('DEAD')

    else:
        print(f"{defender.name} defends successfully against {attacker.name}!")
        if attacker.item:
            defender.equip_item(attacker.item)
        attacker.knight_died('DEAD')


def final_state_to_json(items, knights):
    state = {}
    for knight_object in knights.values():
        state[knight_object.name.lower()] = knight_object.get_info()

    for item_object in items.values():
        state[item_object.name] = item_object.get_info()
        
    return state

def main():
    
    try:
        with open('moves.txt', 'r') as f:
            moves = f.read().splitlines()
    except FileNotFoundError:
        print("Error: The file 'moves.txt' does not exist.")
        return

    if not are_moves_valid(moves):
        print("Error: The file 'moves.txt' does not contain valid set of moves.")
        return
    
    moves = moves[1:-1]
    
    items, knights = initialize_board()

    print("Highlight in Knights Battle:\n")
    process_moves(moves, items, knights)

    final_state = final_state_to_json(items, knights)
    
    print("\nFinal results after the battle is stored in final_state.json file successfully!.")
    with open('final_state.json', 'w') as f:
        json.dump(final_state, f, indent=4)

if __name__ == "__main__":
    main()
