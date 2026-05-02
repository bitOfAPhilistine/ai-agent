
import random

class Player:
    def __init__(self, name="Hero"):
        self.name = name
        self.health = 100
        self.attack = 10
        self.inventory = []
        self.current_room = None

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {damage} damage. Current health: {self.health}")

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 5, self.attack + 5)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {damage} damage. Current health: {self.health}")

    def attack_player(self, player):
        damage = random.randint(self.attack - 3, self.attack + 3)
        print(f"{self.name} attacks {player.name} for {damage} damage!")
        player.take_damage(damage)

class Room:
    def __init__(self, room_id, description):
        self.room_id = room_id
        self.description = description
        self.exits = {}  # e.g., {"north": <RoomObject>}
        self.items = []
        self.enemy = None

    def add_exit(self, direction, room):
        self.exits[direction] = room

    def add_item(self, item):
        self.items.append(item)

    def add_enemy(self, enemy):
        self.enemy = enemy

class Game:
    def __init__(self):
        self.player = Player()
        self.dungeon = self.generate_dungeon(5, 5) # 5x5 dungeon
        self.player.current_room = self.dungeon[0][0] # Start at top-left
        self.current_combat_enemy = None

    def generate_dungeon(self, width, height):
        dungeon_grid = []
        for y in range(height):
            row = []
            for x in range(width):
                room_id = f"room_{x}_{y}"
                description = f"You are in a dusty room at ({x},{y})."
                room = Room(room_id, description)
                row.append(room)
            dungeon_grid.append(row)

        # Connect rooms and add some items/enemies
        for y in range(height):
            for x in range(width):
                room = dungeon_grid[y][x]

                # Connect to adjacent rooms
                if x > 0: # West
                    room.add_exit("west", dungeon_grid[y][x-1])
                    dungeon_grid[y][x-1].add_exit("east", room)
                if y > 0: # North
                    room.add_exit("north", dungeon_grid[y-1][x])
                    dungeon_grid[y-1][x].add_exit("south", room)

                # Randomly add items
                if random.random() < 0.2: # 20% chance for an item
                    room.add_item(random.choice(["health potion", "rusty sword", "gold coin"]))

                # Randomly add enemies (not in starting room)
                if (x != 0 or y != 0) and random.random() < 0.15: # 15% chance for an enemy
                    enemy_name = random.choice(["Goblin", "Orc", "Skeleton"])
                    enemy_health = random.randint(30, 70)
                    enemy_attack = random.randint(5, 15)
                    room.add_enemy(Enemy(enemy_name, enemy_health, enemy_attack))
        return dungeon_grid


    def play(self):
        print("Welcome to the Dungeon Adventure!")
        self.show_room()
        while True:
            command = input("> ").lower().split()
            if not command:
                continue

            if command[0] == "quit":
                print("Thanks for playing!")
                break
            elif command[0] == "go":
                if len(command) > 1:
                    self.move(command[1])
                else:
                    print("Go where?")
            elif command[0] == "look":
                self.show_room()
            elif command[0] == "take":
                if len(command) > 1:
                    self.take_item(command[1])
                else:
                    print("Take what?")
            elif command[0] == "inventory":
                self.show_inventory()
            elif command[0] == "attack" and self.current_combat_enemy:
                self.combat_turn()
            else:
                print("Unknown command or no enemy to attack.")

            if not self.player.is_alive():
                print("You have been defeated! Game Over.")
                break


    def show_room(self):
        room = self.player.current_room
        print("\n" + room.description)
        if room.items:
            print("You see:", ", ".join(room.items))
        if room.enemy and room.enemy.is_alive():
            print(f"A {room.enemy.name} stands here, ready to fight! Health: {room.enemy.health}")
            self.current_combat_enemy = room.enemy
        else:
            self.current_combat_enemy = None
        print("Exits:", ", ".join(room.exits.keys()))

    def move(self, direction):
        room = self.player.current_room
        if direction in room.exits:
            self.player.current_room = room.exits[direction]
            self.show_room()
            if self.current_combat_enemy: # If there's an enemy, combat starts
                print(f"You encounter a {self.current_combat_enemy.name}!")
                # Combat starts automatically when an enemy is present.
                # Player can only 'attack' or 'quit' during combat.
        else:
            print("You can't go that way.")

    def take_item(self, item_name):
        room = self.player.current_room
        if item_name in room.items:
            self.player.inventory.append(item_name)
            room.items.remove(item_name)
            print(f"You picked up the {item_name}.")
        else:
            print(f"There's no {item_name} here.")

    def show_inventory(self):
        if self.player.inventory:
            print("Inventory:", ", ".join(self.player.inventory))
        else:
            print("Your inventory is empty.")

    def combat_turn(self):
        if not self.current_combat_enemy or not self.current_combat_enemy.is_alive():
            print("There is no enemy to attack.")
            self.current_combat_enemy = None
            return

        enemy = self.current_combat_enemy

        # Player's turn
        self.player.attack_enemy(enemy)
        if not enemy.is_alive():
            print(f"You defeated the {enemy.name}!")
            self.player.current_room.enemy = None # Remove defeated enemy from room
            self.current_combat_enemy = None
            self.show_room() # Show room description after combat
            return

        # Enemy's turn
        enemy.attack_player(self.player)
        if not self.player.is_alive():
            return # Game over handled in main loop

if __name__ == "__main__":
    game = Game()
    game.play()
