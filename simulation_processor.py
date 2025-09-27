"""
Simulation data processor for poker games.

This module handles loading and processing of simulation data files,
converting them into human-readable format.
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from card_utils import CardDecoder
from simple_game_display import SimpleGameDisplay


class SimulationProcessor:
    """Processes poker simulation data files."""
    
    def __init__(self):
        """Initialize the simulation processor."""
        self.decoder = CardDecoder()
        self.display = SimpleGameDisplay()
    
    def load_simulation_data(self, simulation_path: str) -> Dict[str, Any]:
        """
        Load simulation data from a directory.
        
        Args:
            simulation_path: Path to simulation directory
            
        Returns:
            Dictionary containing simulation data
        """
        simulation_data = {
            "simulation_id": None,
            "metadata": {},
            "hands": [],
            "actions": [],
            "communication": []
        }
        
        # Load simulation metadata
        meta_file = os.path.join(simulation_path, "simulation_meta.json")
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                simulation_data["metadata"] = json.load(f)
                simulation_data["simulation_id"] = simulation_data["metadata"].get("simulation_id")
        
        # Load game logs
        game_logs_dir = os.path.join(simulation_path, "game_logs")
        if os.path.exists(game_logs_dir):
            for filename in os.listdir(game_logs_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(game_logs_dir, filename)
                    with open(file_path, 'r') as f:
                        hand_data = json.load(f)
                        simulation_data["hands"].append(hand_data)
        
        # Load communication data
        chat_logs_dir = os.path.join(simulation_path, "chat_logs")
        if os.path.exists(chat_logs_dir):
            for filename in os.listdir(chat_logs_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(chat_logs_dir, filename)
                    with open(file_path, 'r') as f:
                        comm_data = json.load(f)
                        simulation_data["communication"].append(comm_data)
        
        # Load conversation data
        chat_dataset_dir = os.path.join(simulation_path, "chat_dataset")
        if os.path.exists(chat_dataset_dir):
            conversations_file = os.path.join(chat_dataset_dir, "conversations.json")
            if os.path.exists(conversations_file):
                with open(conversations_file, 'r') as f:
                    simulation_data["conversations"] = json.load(f)
            
            game_contexts_file = os.path.join(chat_dataset_dir, "game_contexts.json")
            if os.path.exists(game_contexts_file):
                with open(game_contexts_file, 'r') as f:
                    simulation_data["game_contexts"] = json.load(f)
        
        return simulation_data
    
    def process_simulation(self, simulation_path: str) -> Dict[str, Any]:
        """
        Process a complete simulation and create human-readable output.
        
        Args:
            simulation_path: Path to simulation directory
            
        Returns:
            Dictionary containing processed simulation data
        """
        # Load raw data
        raw_data = self.load_simulation_data(simulation_path)
        
        # Process the data
        processed_data = {
            "simulation_id": raw_data["simulation_id"],
            "metadata": raw_data["metadata"],
            "summary": self._create_simulation_summary(raw_data),
            "hands": self._process_hands(raw_data["hands"]),
            "communication": self._process_communication(raw_data.get("communication", [])),
            "human_readable": self._create_human_readable_output(raw_data)
        }
        
        return processed_data
    
    def _create_simulation_summary(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of the simulation."""
        metadata = raw_data.get("metadata", {})
        
        return {
            "simulation_id": metadata.get("simulation_id"),
            "start_time": metadata.get("start_time"),
            "end_time": metadata.get("end_time"),
            "status": metadata.get("status"),
            "total_hands": metadata.get("final_stats", {}).get("total_hands", 0),
            "final_chips": metadata.get("final_stats", {}).get("final_chips", {}),
            "collusion_players": metadata.get("final_stats", {}).get("collusion_players", []),
            "llm_players": metadata.get("final_stats", {}).get("llm_players", [])
        }
    
    def _process_hands(self, hands_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process hand data to make it human-readable."""
        processed_hands = []
        
        for hand in hands_data:
            processed_hand = {
                "hand_id": hand.get("hand_id"),
                "phase": hand.get("phase"),
                "timestamp": hand.get("timestamp"),
                "player_id": hand.get("player_id"),
                "action_type": hand.get("action_type"),
                "amount": hand.get("amount"),
                "reason": hand.get("reason"),
                "game_state": self._process_game_state(hand.get("game_state", {}))
            }
            processed_hands.append(processed_hand)
        
        return processed_hands
    
    def _process_game_state(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process game state to make cards human-readable."""
        processed_state = game_state.copy()
        
        # Process community cards
        if "community_cards" in game_state:
            community_cards = game_state["community_cards"]
            if community_cards:
                decoded_community = self.decoder.decode_community_cards(community_cards)
                processed_state["community_cards_readable"] = decoded_community
        
        # Process player hands
        if "players" in game_state:
            processed_players = {}
            for player_id, player_info in game_state["players"].items():
                processed_player = player_info.copy()
                
                # Decode hole cards
                hand_cards = player_info.get("hand_cards", [])
                if hand_cards:
                    decoded_hand = self.decoder.decode_hand(hand_cards)
                    processed_player["hand_cards_readable"] = decoded_hand
                
                processed_players[player_id] = processed_player
            
            processed_state["players"] = processed_players
        
        return processed_state
    
    def _process_communication(self, communication_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process communication data."""
        processed_comm = []
        
        for comm in communication_data:
            processed_comm.append({
                "timestamp": comm.get("timestamp"),
                "hand_id": comm.get("hand_id"),
                "phase": comm.get("phase"),
                "player_id": comm.get("player_id"),
                "message": comm.get("message"),
                "message_type": comm.get("message_type"),
                "contains_signal": comm.get("contains_signal", False)
            })
        
        return processed_comm
    
    def _create_human_readable_output(self, raw_data: Dict[str, Any]) -> str:
        """Create human-readable output for the entire simulation."""
        output = []
        
        # Simulation header
        metadata = raw_data.get("metadata", {})
        sim_id = metadata.get("simulation_id", "Unknown")
        output.append(f"=== POKER SIMULATION {sim_id} ===")
        output.append("")
        
        # Simulation summary
        summary = self._create_simulation_summary(raw_data)
        output.append("SIMULATION SUMMARY:")
        output.append(f"  Start Time: {summary.get('start_time', 'Unknown')}")
        output.append(f"  End Time: {summary.get('end_time', 'Unknown')}")
        output.append(f"  Status: {summary.get('status', 'Unknown')}")
        output.append(f"  Total Hands: {summary.get('total_hands', 0)}")
        output.append("")
        
        # Final chip counts
        final_chips = summary.get("final_chips", {})
        if final_chips:
            output.append("FINAL CHIP COUNTS:")
            for player_id, chips in final_chips.items():
                output.append(f"  Player {player_id}: {chips} chips")
            output.append("")
        
        # Process each hand
        hands_data = raw_data.get("hands", [])
        if hands_data:
            output.append("HAND-BY-HAND BREAKDOWN:")
            output.append("")
            
            # Group hands by hand_id
            hands_by_id = {}
            for hand in hands_data:
                hand_id = hand.get("hand_id", "unknown")
                if hand_id not in hands_by_id:
                    hands_by_id[hand_id] = []
                hands_by_id[hand_id].append(hand)
            
            # Display each hand
            for hand_id in sorted(hands_by_id.keys(), key=lambda x: int(x) if x.isdigit() else 0):
                hand_actions = hands_by_id[hand_id]
                output.append(f"--- HAND {hand_id} ---")
                
                for action in hand_actions:
                    action_summary = self.display.display_action_summary(action)
                    output.append(action_summary)
                    output.append("")
        
        return "\n".join(output)
    
    def save_processed_simulation(self, simulation_path: str, output_path: str = None) -> str:
        """
        Process a simulation and save the human-readable output.
        
        Args:
            simulation_path: Path to simulation directory
            output_path: Optional output path
            
        Returns:
            Path to the saved file
        """
        # Process the simulation
        processed_data = self.process_simulation(simulation_path)
        
        # Create output filename
        if output_path is None:
            sim_id = processed_data.get("simulation_id", "unknown")
            output_path = f"simulation_{sim_id}_decoded.txt"
        
        # Save human-readable output
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_data["human_readable"])
        
        # Save processed JSON data
        json_output_path = output_path.replace('.txt', '.json')
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, default=str)
        
        return output_path
    
    def process_multiple_simulations(self, simulations_dir: str, output_dir: str = None) -> List[str]:
        """
        Process multiple simulations in a directory.
        
        Args:
            simulations_dir: Directory containing simulation subdirectories
            output_dir: Directory to save processed files
            
        Returns:
            List of paths to processed files
        """
        if output_dir is None:
            output_dir = "processed_simulations"
        
        os.makedirs(output_dir, exist_ok=True)
        
        processed_files = []
        
        # Find all simulation directories
        for item in os.listdir(simulations_dir):
            item_path = os.path.join(simulations_dir, item)
            if os.path.isdir(item_path) and item.startswith("simulation_"):
                try:
                    # Process this simulation
                    output_file = self.save_processed_simulation(
                        item_path, 
                        os.path.join(output_dir, f"{item}_decoded.txt")
                    )
                    processed_files.append(output_file)
                    print(f"Processed simulation: {item}")
                except Exception as e:
                    print(f"Error processing simulation {item}: {e}")
        
        return processed_files


# Example usage and testing
if __name__ == "__main__":
    # Test the processor
    processor = SimulationProcessor()
    
    # Example usage
    print("Simulation Processor initialized")
    print("Use processor.process_simulation(path) to process a simulation")
    print("Use processor.save_processed_simulation(path) to save output")
