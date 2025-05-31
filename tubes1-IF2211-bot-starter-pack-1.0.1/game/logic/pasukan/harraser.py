from abc import ABC
from typing import Optional, List, Tuple
import random
from game.logic.base import BaseLogic
from game.models import Board, GameObject, Position
from ...util import *
import math


class Perusuh(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.last_position: Optional[Position] = None
        self.stuck_counter = 0
    
    def calculate_distance(self, pos1: Position, pos2: Position) -> int:
        return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
    
    def get_movement_direction(self, current_pos: Position, target_pos: Position) -> Tuple[int, int]:
        delta_x = clamp(target_pos.x - current_pos.x, -1, 1)
        delta_y = clamp(target_pos.y - current_pos.y, -1, 1)
        
        if delta_x != 0:
            delta_y = 0
            
        if delta_x == 0 and delta_y == 0:
            return self._get_edge_movement(current_pos)
        
        return delta_x, delta_y
    
    def _get_edge_movement(self, current_pos: Position) -> Tuple[int, int]:
        board_size = 15
        
        if current_pos.x == 0:
            return (1, 0)
        elif current_pos.x == board_size - 1:
            return (-1, 0)
        elif current_pos.y == 0:
            return (0, 1)
        elif current_pos.y == board_size - 1:
            return (0, -1)
        else:
            return (-1, 0)
    
    def get_block_coordinates(self, position: Position, block_size: int = 5) -> Tuple[int, int]:
        block_x = position.x // block_size
        block_y = position.y // block_size
        return block_x, block_y
    
    def get_block_bounds(self, block_x: int, block_y: int, block_size: int = 5) -> Tuple[int, int, int, int]:
        start_x = block_x * block_size
        end_x = (block_x + 1) * block_size
        start_y = block_y * block_size
        end_y = (block_y + 1) * block_size
        return start_x, end_x, start_y, end_y
    
    def find_targets_in_current_block(self, board: Board, current_pos: Position, 
                                    my_bot_name: str, min_diamonds: int = 2) -> List[GameObject]:
        block_x, block_y = self.get_block_coordinates(current_pos)
        start_x, end_x, start_y, end_y = self.get_block_bounds(block_x, block_y)
        
        targets = []
        for game_obj in board.game_objects:
            if (hasattr(game_obj, 'properties') and 
                hasattr(game_obj.properties, 'can_tackle') and
                game_obj.properties.can_tackle and
                game_obj.properties.diamonds >= min_diamonds and
                game_obj.properties.name != my_bot_name and
                start_x <= game_obj.position.x < end_x and
                start_y <= game_obj.position.y < end_y):
                targets.append(game_obj)
        
        return targets
    
    def find_best_target_in_current_block(self, board: Board, current_pos: Position, 
                                        my_bot_name: str) -> Optional[Position]:
        targets = self.find_targets_in_current_block(board, current_pos, my_bot_name)
        
        if not targets:
            return None
        
        targets.sort(key=lambda bot: (
            self.calculate_distance(current_pos, bot.position),
            -bot.properties.diamonds
        ))
        
        return targets[0].position
    
    def analyze_all_blocks(self, board: Board, current_pos: Position, 
                          my_bot_name: str, base_pos: Position) -> Optional[Position]:
        block_data = []
        
        for i in range(3):
            for j in range(3):
                start_x, end_x, start_y, end_y = self.get_block_bounds(i, j)
                
                total_diamonds = 0
                targets_in_block = []
                
                for game_obj in board.game_objects:
                    if (hasattr(game_obj, 'properties') and 
                        hasattr(game_obj.properties, 'can_tackle') and
                        game_obj.properties.can_tackle and
                        game_obj.properties.diamonds >= 2 and
                        game_obj.properties.name != my_bot_name and
                        start_x <= game_obj.position.x < end_x and
                        start_y <= game_obj.position.y < end_y):
                        
                        total_diamonds += game_obj.properties.diamonds
                        distance = self.calculate_distance(current_pos, game_obj.position)
                        targets_in_block.append((distance, game_obj.position, game_obj.properties.diamonds))
                
                if targets_in_block:
                    targets_in_block.sort(key=lambda x: x[0])
                    nearest_distance, nearest_pos, diamonds = targets_in_block[0]
                    
                    priority = total_diamonds / max(1, nearest_distance)
                    block_data.append((priority, nearest_distance, nearest_pos, total_diamonds))
        
        if not block_data:
            return base_pos
        
        block_data.sort(key=lambda x: x[0], reverse=True)
        _, _, best_target_pos, _ = block_data[0]
        
        return best_target_pos
    
    def find_diamonds_on_board(self, board: Board) -> List[GameObject]:
        diamonds = []
        for game_obj in board.game_objects:
            if (hasattr(game_obj, 'type') and game_obj.type == 'DiamondGameObject') or \
               (not hasattr(game_obj, 'properties') or not hasattr(game_obj.properties, 'can_tackle')):
                if not hasattr(game_obj, 'properties') or not hasattr(game_obj.properties, 'name'):
                    diamonds.append(game_obj)
        
        return diamonds
    
    def find_nearest_diamond(self, board: Board, current_pos: Position) -> Optional[Position]:
        diamonds = self.find_diamonds_on_board(board)
        
        if not diamonds:
            return None
        
        diamonds_with_distance = []
        for diamond in diamonds:
            distance = self.calculate_distance(current_pos, diamond.position)
            diamonds_with_distance.append((distance, diamond.position))
        
        diamonds_with_distance.sort(key=lambda x: x[0])
        
        return diamonds_with_distance[0][1]
    
    def find_diamonds_in_current_block(self, board: Board, current_pos: Position) -> List[GameObject]:
        block_x, block_y = self.get_block_coordinates(current_pos)
        start_x, end_x, start_y, end_y = self.get_block_bounds(block_x, block_y)
        
        diamonds = []
        for game_obj in board.game_objects:
            if ((hasattr(game_obj, 'type') and game_obj.type == 'DiamondGameObject') or \
                (not hasattr(game_obj, 'properties') or not hasattr(game_obj.properties, 'can_tackle'))) and \
               start_x <= game_obj.position.x < end_x and \
               start_y <= game_obj.position.y < end_y:
                diamonds.append(game_obj)
        
        return diamonds
    
    def find_best_diamond_in_current_block(self, board: Board, current_pos: Position) -> Optional[Position]:
        diamonds = self.find_diamonds_in_current_block(board, current_pos)
        
        if not diamonds:
            return None
        
        diamonds.sort(key=lambda diamond: self.calculate_distance(current_pos, diamond.position))
        
        return diamonds[0].position
    
    def analyze_diamond_blocks(self, board: Board, current_pos: Position) -> Optional[Position]:
        block_data = []
        
        for i in range(3):
            for j in range(3):
                start_x, end_x, start_y, end_y = self.get_block_bounds(i, j)
                
                diamonds_in_block = []
                
                for game_obj in board.game_objects:
                    if ((hasattr(game_obj, 'type') and game_obj.type == 'DiamondGameObject') or \
                        (not hasattr(game_obj, 'properties') or not hasattr(game_obj.properties, 'can_tackle'))) and \
                       start_x <= game_obj.position.x < end_x and \
                       start_y <= game_obj.position.y < end_y:
                        
                        distance = self.calculate_distance(current_pos, game_obj.position)
                        diamonds_in_block.append((distance, game_obj.position))
                
                if diamonds_in_block:
                    diamonds_in_block.sort(key=lambda x: x[0])
                    nearest_distance, nearest_pos = diamonds_in_block[0]
                    
                    diamond_count = len(diamonds_in_block)
                    priority = diamond_count / max(1, nearest_distance)
                    block_data.append((priority, nearest_distance, nearest_pos, diamond_count))
        
        if not block_data:
            return None
        
        block_data.sort(key=lambda x: x[0], reverse=True)
        _, _, best_diamond_pos, _ = block_data[0]
        
        return best_diamond_pos
    
    def should_return_to_base(self, bot_props, current_pos: Position, base_pos: Position) -> bool:
        distance_to_base = self.calculate_distance(current_pos, base_pos)
        time_left_seconds = bot_props.milliseconds_left / 1000
        
        if bot_props.diamonds >= 4:
            return True
        
        if (distance_to_base + 1 >= time_left_seconds and bot_props.diamonds > 0) or \
           (distance_to_base >= time_left_seconds):
            return True
        
        return False
    
    def detect_stuck_state(self, current_pos: Position):
        if (self.last_position and 
            current_pos.x == self.last_position.x and 
            current_pos.y == self.last_position.y):
            self.stuck_counter += 1
        else:
            self.stuck_counter = 0
        
        self.last_position = current_pos
    
    def get_random_movement(self) -> Tuple[int, int]:
        if self.stuck_counter > 3:
            self.current_direction = (self.current_direction + 1) % len(self.directions)
        elif random.random() > 0.7:
            self.current_direction = random.randint(0, len(self.directions) - 1)
        
        return self.directions[self.current_direction]
    
    def next_move(self, board_bot: GameObject, board: Board) -> Tuple[int, int]:
        props = board_bot.properties
        my_bot_name = props.name
        base_pos = props.base
        current_pos = board_bot.position
        
        time_left = props.milliseconds_left / 1000
        print(f"Time left: {time_left:.1f} sec")
        print(f"Diamonds: {props.diamonds}")
        print(f"Position: ({current_pos.x}, {current_pos.y})")
        
        self.detect_stuck_state(current_pos)
        
        if self.should_return_to_base(props, current_pos, base_pos):
            print("Returning to base")
            self.goal_position = base_pos
        else:
            target_in_current_block = self.find_best_target_in_current_block(
                board, current_pos, my_bot_name
            )
            
            if target_in_current_block:
                print("Targeting enemy in current block")
                self.goal_position = target_in_current_block
            else:
                target_in_other_blocks = self.analyze_all_blocks(
                    board, current_pos, my_bot_name, base_pos
                )
                
                if target_in_other_blocks and target_in_other_blocks != base_pos:
                    print("Targeting enemy in other blocks")
                    self.goal_position = target_in_other_blocks
                else:
                    diamond_in_current_block = self.find_best_diamond_in_current_block(
                        board, current_pos
                    )
                    
                    if diamond_in_current_block:
                        print("Collecting diamond in current block")
                        self.goal_position = diamond_in_current_block
                    else:
                        diamond_in_other_blocks = self.analyze_diamond_blocks(
                            board, current_pos
                        )
                        
                        if diamond_in_other_blocks:
                            print("Moving to diamond in other blocks")
                            self.goal_position = diamond_in_other_blocks
                        else:
                            nearest_diamond = self.find_nearest_diamond(board, current_pos)
                            
                            if nearest_diamond:
                                print("Moving to nearest diamond on board")
                                self.goal_position = nearest_diamond
                            else:
                                print("No diamonds or targets found, staying at base")
                                self.goal_position = base_pos
        
        if self.goal_position:
            print(f"Goal: ({self.goal_position.x}, {self.goal_position.y})")
            delta_x, delta_y = self.get_movement_direction(current_pos, self.goal_position)
        else:
            print("Random movement")
            delta_x, delta_y = self.get_random_movement()
        
        if self.stuck_counter > 5:
            print("Stuck! Random movement")
            delta_x, delta_y = self.get_random_movement()
        
        return delta_x, delta_y