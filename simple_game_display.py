"""
Simple game display that outputs exactly the format requested.

This module provides the specific output format:
Hand X - phase:
player0: K of Spades (K♠), Q of Hearts (Q♥) & [has X amount of chips left]
board: [cards on board]
BB: [who is BB]
SB: [who is SB]
Actions:
player0: "[chat message]" & [action]
"""

from typing import Dict, List, Any, Optional
from card_utils import CardDecoder


class SimpleGameDisplay:
    """Handles display of poker games in the exact format requested."""
    
    def __init__(self):
        """Initialize the simple game display."""
        self.decoder = CardDecoder()
    
    def format_card_for_display(self, card_data: Dict[str, int]) -> str:
        """Format a single card for display."""
        decoded = self.decoder.decode_card(card_data["rank"], card_data["suit"])
        return f"{decoded['full_name']} ({decoded['display']})"
    
    def format_hand_for_display(self, hand_cards: List[Dict[str, int]]) -> str:
        """Format a player's hand for display."""
        if not hand_cards:
            return "No cards"
        
        formatted_cards = []
        for card in hand_cards:
            formatted_cards.append(self.format_card_for_display(card))
        
        return ", ".join(formatted_cards)
    
    def format_community_cards_for_display(self, community_cards: List[Dict[str, int]]) -> str:
        """Format community cards for display."""
        if not community_cards:
            return "No community cards"
        
        formatted_cards = []
        for card in community_cards:
            formatted_cards.append(self.format_card_for_display(card))
        
        return ", ".join(formatted_cards)
    
    def get_player_position_info(self, player_info: Dict[str, Any]) -> str:
        """Get position information for a player."""
        position = player_info.get("position", "Unknown")
        is_button = player_info.get("is_button", False)
        is_small_blind = player_info.get("is_small_blind", False)
        is_big_blind = player_info.get("is_big_blind", False)
        
        if is_button:
            return f"{position} (Button)"
        elif is_small_blind:
            return f"{position} (SB)"
        elif is_big_blind:
            return f"{position} (BB)"
        else:
            return position
    
    def format_action_for_display(self, action: Dict[str, Any]) -> str:
        """Format an action for display."""
        action_type = action.get("action_type", "Unknown")
        amount = action.get("amount")
        
        if action_type == "FOLD":
            return "folded"
        elif action_type == "CHECK":
            return "checked"
        elif action_type == "CALL":
            if amount:
                return f"called {amount}"
            else:
                return "called"
        elif action_type == "RAISE":
            if amount:
                return f"raised {amount}"
            else:
                return "raised"
        else:
            return action_type.lower()
    
    def display_hand_phase(self, hand_data: Dict[str, Any], phase: str, 
                          communication_data: List[Dict[str, Any]] = None) -> str:
        """
        Display a specific phase of a hand in the requested format.
        
        Args:
            hand_data: Dictionary containing hand data
            phase: Phase name (PREFLOP, FLOP, TURN, RIVER)
            communication_data: List of communication messages for this hand/phase
            
        Returns:
            Formatted string for this hand phase
        """
        output = []
        
        # Hand header
        hand_id = hand_data.get("hand_id", "Unknown")
        output.append(f"Hand {hand_id} - {phase.lower()}:")
        
        # Get game state
        game_state = hand_data.get("game_state", {})
        players = game_state.get("players", {})
        
        # Display each player's cards and chips
        for player_id in sorted(players.keys(), key=int):
            player_info = players[player_id]
            hand_cards = player_info.get("hand_cards", [])
            chips = player_info.get("chips", 0)
            
            # Format hand cards
            hand_display = self.format_hand_for_display(hand_cards)
            
            # Add to output
            output.append(f"player{player_id}: {hand_display} & [has {chips} chips left]")
        
        # Display board cards
        community_cards = game_state.get("community_cards", [])
        board_display = self.format_community_cards_for_display(community_cards)
        output.append(f"board: {board_display}")
        
        # Display button positions
        button_position = game_state.get("button_position")
        small_blind_position = game_state.get("small_blind_position")
        big_blind_position = game_state.get("big_blind_position")
        
        if big_blind_position is not None:
            output.append(f"BB: player{big_blind_position}")
        if small_blind_position is not None:
            output.append(f"SB: player{small_blind_position}")
        
        # Display actions and communication
        output.append("Actions:")
        
        # Get betting history for this phase
        betting_history = game_state.get("betting_history", [])
        phase_actions = []
        for phase_info in betting_history:
            if phase_info.get("phase", "").upper() == phase.upper():
                phase_actions = phase_info.get("actions", [])
                break
        
        # Get communication for this hand/phase
        communication_messages = []
        if communication_data:
            for comm in communication_data:
                if (comm.get("hand_id") == hand_id and 
                    comm.get("phase", "").upper() == phase.upper()):
                    communication_messages.append(comm)
        
        # Create a mapping of player actions and messages
        player_actions = {}
        for action in phase_actions:
            player_id = action.get("player_id")
            if player_id not in player_actions:
                player_actions[player_id] = []
            player_actions[player_id].append(action)
        
        player_messages = {}
        for comm in communication_messages:
            player_id = comm.get("player_id")
            if player_id not in player_messages:
                player_messages[player_id] = []
            player_messages[player_id].append(comm)
        
        # Display actions for each player
        for player_id in sorted(players.keys(), key=int):
            player_info = players[player_id]
            player_id_str = str(player_id)
            
            # Get player's message
            message = ""
            if player_id_str in player_messages:
                # Get the most recent message for this player
                recent_message = player_messages[player_id_str][-1]
                message = recent_message.get("message", "")
            
            # Get player's action
            action_display = ""
            if player_id_str in player_actions:
                # Get the most recent action for this player
                recent_action = player_actions[player_id_str][-1]
                action_display = self.format_action_for_display(recent_action)
            else:
                action_display = "no action"
            
            # Format the line
            if message:
                output.append(f"player{player_id}: \"{message}\" & {action_display}")
            else:
                output.append(f"player{player_id}: \"\" & {action_display}")
        
        return "\n".join(output)
    
    def display_complete_hand(self, hand_data: Dict[str, Any], 
                             communication_data: List[Dict[str, Any]] = None) -> str:
        """
        Display a complete hand with all phases.
        
        Args:
            hand_data: Dictionary containing hand data
            communication_data: List of communication messages
            
        Returns:
            Formatted string for the complete hand
        """
        output = []
        
        # Get the phases that occurred in this hand
        game_state = hand_data.get("game_state", {})
        betting_history = game_state.get("betting_history", [])
        
        phases = []
        for phase_info in betting_history:
            phase_name = phase_info.get("phase", "").upper()
            if phase_name and phase_name not in phases:
                phases.append(phase_name)
        
        # If no betting history, assume PREFLOP
        if not phases:
            phases = ["PREFLOP"]
        
        # Display each phase
        for phase in phases:
            phase_output = self.display_hand_phase(hand_data, phase, communication_data)
            output.append(phase_output)
            output.append("")  # Empty line between phases
        
        return "\n".join(output)
    
    def display_simulation(self, simulation_data: Dict[str, Any]) -> str:
        """
        Display a complete simulation.
        
        Args:
            simulation_data: Dictionary containing simulation data
            
        Returns:
            Formatted string for the complete simulation
        """
        output = []
        
        # Get simulation metadata
        metadata = simulation_data.get("metadata", {})
        sim_id = metadata.get("simulation_id", "Unknown")
        
        output.append(f"=== POKER SIMULATION {sim_id} ===")
        output.append("")
        
        # Get hands data
        hands_data = simulation_data.get("hands", [])
        communication_data = simulation_data.get("communication", [])
        
        if not hands_data:
            output.append("No hands found in simulation data.")
            return "\n".join(output)
        
        # Group hands by hand_id
        hands_by_id = {}
        for hand in hands_data:
            hand_id = hand.get("hand_id", "unknown")
            if hand_id not in hands_by_id:
                hands_by_id[hand_id] = []
            hands_by_id[hand_id].append(hand)
        
        # Display each hand
        for hand_id in sorted(hands_by_id.keys(), key=lambda x: int(x) if str(x).isdigit() else 0):
            hand_actions = hands_by_id[hand_id]
            
            # Use the first action as the representative hand data
            representative_hand = hand_actions[0]
            
            # Get communication for this hand
            hand_communication = []
            if communication_data:
                for comm in communication_data:
                    if comm.get("hand_id") == hand_id:
                        hand_communication.append(comm)
            
            # Display the complete hand
            hand_output = self.display_complete_hand(representative_hand, hand_communication)
            output.append(hand_output)
            output.append("")  # Empty line between hands
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    # Test the simple display
    display = SimpleGameDisplay()
    
    # Example hand data
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
    
    # Display the hand
    hand_output = display.display_hand_phase(example_hand, "PREFLOP", example_communication)
    print(hand_output)
