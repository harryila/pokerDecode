"""
Simple poker decoder that outputs exactly the requested format.

This decoder processes simulation data and outputs it in the specific format:
Hand X - phase:
player0: K of Spades (K♠), Q of Hearts (Q♥) & [has X amount of chips left]
board: [cards on board]
BB: [who is BB]
SB: [who is SB]
Actions:
player0: "[chat message]" & [action]
"""

import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path

from card_utils import CardDecoder
from simple_game_display import SimpleGameDisplay
from simulation_processor import SimulationProcessor


class SimplePokerDecoder:
    """
    Simple poker decoder that outputs the exact format requested.
    """
    
    def __init__(self):
        """Initialize the simple poker decoder."""
        self.decoder = CardDecoder()
        self.display = SimpleGameDisplay()
        self.processor = SimulationProcessor()
    
    def decode_simulation(self, simulation_path: str, output_path: str = None) -> str:
        """
        Decode a complete simulation into the requested format.
        
        Args:
            simulation_path: Path to simulation directory
            output_path: Optional path to save output file
            
        Returns:
            Path to the decoded output file
        """
        # Load simulation data
        simulation_data = self.processor.load_simulation_data(simulation_path)
        
        # Create the formatted output
        formatted_output = self.display.display_simulation(simulation_data)
        
        # Create output filename
        if output_path is None:
            sim_id = simulation_data.get("simulation_id", "unknown")
            output_path = f"simulation_{sim_id}_simple_format.txt"
        
        # Save the output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_output)
        
        return output_path
    
    def decode_single_hand(self, hand_data: Dict[str, Any], 
                          communication_data: List[Dict[str, Any]] = None) -> str:
        """
        Decode a single hand into the requested format.
        
        Args:
            hand_data: Dictionary containing hand data
            communication_data: List of communication messages
            
        Returns:
            Formatted string for the hand
        """
        return self.display.display_complete_hand(hand_data, communication_data)
    
    def decode_hand_phase(self, hand_data: Dict[str, Any], phase: str,
                         communication_data: List[Dict[str, Any]] = None) -> str:
        """
        Decode a specific phase of a hand.
        
        Args:
            hand_data: Dictionary containing hand data
            phase: Phase name (PREFLOP, FLOP, TURN, RIVER)
            communication_data: List of communication messages
            
        Returns:
            Formatted string for the hand phase
        """
        return self.display.display_hand_phase(hand_data, phase, communication_data)
    
    def process_multiple_simulations(self, simulations_dir: str, output_dir: str = None) -> List[str]:
        """
        Process multiple simulations in the simple format.
        
        Args:
            simulations_dir: Directory containing simulation subdirectories
            output_dir: Directory to save processed files
            
        Returns:
            List of paths to processed files
        """
        if output_dir is None:
            output_dir = "simple_processed_simulations"
        
        os.makedirs(output_dir, exist_ok=True)
        
        processed_files = []
        
        # Find all simulation directories
        for item in os.listdir(simulations_dir):
            item_path = os.path.join(simulations_dir, item)
            if os.path.isdir(item_path) and item.startswith("simulation_"):
                try:
                    # Process this simulation
                    output_file = self.decode_simulation(
                        item_path, 
                        os.path.join(output_dir, f"{item}_simple_format.txt")
                    )
                    processed_files.append(output_file)
                    print(f"Processed simulation: {item}")
                except Exception as e:
                    print(f"Error processing simulation {item}: {e}")
        
        return processed_files
    
    def load_and_display_simulation(self, simulation_path: str) -> str:
        """
        Load a simulation and return the simple format display.
        
        Args:
            simulation_path: Path to simulation directory
            
        Returns:
            Simple format string representation of the simulation
        """
        # Load simulation data
        simulation_data = self.processor.load_simulation_data(simulation_path)
        
        # Create the formatted output
        return self.display.display_simulation(simulation_data)


# Example usage and testing
if __name__ == "__main__":
    # Initialize the simple decoder
    decoder = SimplePokerDecoder()
    
    # Example usage
    print("Simple Poker Decoder initialized")
    print("Available methods:")
    print("  - decode_simulation(path): Decode a complete simulation")
    print("  - decode_single_hand(hand_data): Decode a single hand")
    print("  - decode_hand_phase(hand_data, phase): Decode a hand phase")
    print("  - process_multiple_simulations(dir): Process multiple simulations")
    
    # Test with example data
    example_hand = {
        "hand_id": 1,
        "phase": "PREFLOP",
        "game_state": {
            "hand_id": 1,
            "pot_amount": 15,
            "community_cards": [],
            "players": {
                "0": {
                    "chips": 490,
                    "state": "TO_CALL",
                    "position": "SB",
                    "hand_cards": [
                        {"rank": 11, "suit": 1},  # King of Spades
                        {"rank": 10, "suit": 2}   # Queen of Hearts
                    ],
                    "is_small_blind": True,
                    "is_big_blind": False
                },
                "1": {
                    "chips": 485,
                    "state": "IN",
                    "position": "BB",
                    "hand_cards": [
                        {"rank": 0, "suit": 2},   # 2 of Hearts
                        {"rank": 1, "suit": 2}    # 3 of Hearts
                    ],
                    "is_small_blind": False,
                    "is_big_blind": True
                }
            },
            "betting_history": [
                {
                    "phase": "preflop",
                    "actions": [
                        {
                            "player_id": 0,
                            "action_type": "RAISE",
                            "amount": 10
                        }
                    ]
                }
            ],
            "button_position": 1,
            "small_blind_position": 0,
            "big_blind_position": 1
        }
    }
    
    # Example communication data
    example_communication = [
        {
            "hand_id": 1,
            "phase": "PREFLOP",
            "player_id": 0,
            "message": "I'm feeling lucky today!"
        }
    ]
    
    # Test the decoder
    print("\n=== TESTING SIMPLE DECODER ===")
    hand_output = decoder.decode_single_hand(example_hand, example_communication)
    print(hand_output)
