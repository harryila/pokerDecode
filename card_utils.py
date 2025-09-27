"""
Card encoding and decoding utilities for poker game data.

This module provides functions to convert between encoded card representations
and human-readable card descriptions.
"""

from typing import Dict, List, Tuple, Union


class CardDecoder:
    """Handles decoding of poker cards from encoded format to human-readable format."""
    
    # Card rank mappings - EXACTLY as used in the texasholdem library
    # From texasholdem/texasholdem/card/card.py: STR_RANKS = "23456789TJQKA"
    RANK_TO_STRING = {
        0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 7: "9", 
        8: "T", 9: "J", 10: "Q", 11: "K", 12: "A"
    }
    
    STRING_TO_RANK = {v: k for k, v in RANK_TO_STRING.items()}
    
    # Suit mappings - EXACTLY as used in the texasholdem library
    # From texasholdem/texasholdem/card/card.py:
    # CHAR_SUIT_TO_INT_SUIT = {"s": 1, "h": 2, "d": 4, "c": 8}
    # PRETTY_SUITS = {1: "♠", 2: "♥", 4: "♦", 8: "♣"}
    SUIT_TO_STRING = {
        1: "Spades", 2: "Hearts", 4: "Diamonds", 8: "Clubs"
    }
    
    SUIT_TO_SYMBOL = {
        1: "♠", 2: "♥", 4: "♦", 8: "♣"
    }
    
    SUIT_TO_SHORT = {
        1: "s", 2: "h", 4: "d", 8: "c"
    }
    
    def __init__(self):
        """Initialize the card decoder."""
        pass
    
    def decode_card(self, rank: int, suit: int) -> Dict[str, str]:
        """
        Decode a single card from encoded format to human-readable format.
        
        Args:
            rank: Card rank (0-12)
            suit: Card suit (1, 2, 4, 8)
            
        Returns:
            Dictionary with decoded card information
        """
        if rank not in self.RANK_TO_STRING:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in self.SUIT_TO_STRING:
            raise ValueError(f"Invalid suit: {suit}")
        
        rank_str = self.RANK_TO_STRING[rank]
        suit_str = self.SUIT_TO_STRING[suit]
        suit_symbol = self.SUIT_TO_SYMBOL[suit]
        suit_short = self.SUIT_TO_SHORT[suit]
        
        return {
            "rank": rank_str,
            "suit": suit_str,
            "symbol": suit_symbol,
            "short": suit_short,
            "display": f"{rank_str}{suit_short}",
            "full_name": f"{rank_str} of {suit_str}",
            "pretty": f"{rank_str}{suit_symbol}"
        }
    
    def decode_card_list(self, cards: List[Dict[str, int]]) -> List[Dict[str, str]]:
        """
        Decode a list of cards from encoded format.
        
        Args:
            cards: List of card dictionaries with 'rank' and 'suit' keys
            
        Returns:
            List of decoded card dictionaries
        """
        return [self.decode_card(card["rank"], card["suit"]) for card in cards]
    
    def decode_hand(self, hand_cards: List[Dict[str, int]]) -> Dict[str, any]:
        """
        Decode a player's hole cards.
        
        Args:
            hand_cards: List of hole cards in encoded format
            
        Returns:
            Dictionary with decoded hand information
        """
        if not hand_cards:
            return {"cards": [], "display": "No cards", "full_names": []}
        
        decoded_cards = self.decode_card_list(hand_cards)
        
        return {
            "cards": decoded_cards,
            "display": " ".join([card["display"] for card in decoded_cards]),
            "full_names": [card["full_name"] for card in decoded_cards],
            "pretty": " ".join([card["pretty"] for card in decoded_cards])
        }
    
    def decode_community_cards(self, community_cards: List[Dict[str, int]]) -> Dict[str, any]:
        """
        Decode community cards (flop, turn, river).
        
        Args:
            community_cards: List of community cards in encoded format
            
        Returns:
            Dictionary with decoded community cards information
        """
        if not community_cards:
            return {"cards": [], "display": "No community cards", "full_names": []}
        
        decoded_cards = self.decode_card_list(community_cards)
        
        return {
            "cards": decoded_cards,
            "display": " ".join([card["display"] for card in decoded_cards]),
            "full_names": [card["full_name"] for card in decoded_cards],
            "pretty": " ".join([card["pretty"] for card in decoded_cards])
        }
    
    def get_hand_strength_description(self, hand_cards: List[Dict[str, int]], 
                                    community_cards: List[Dict[str, int]] = None) -> str:
        """
        Get a basic description of hand strength (simplified).
        
        Args:
            hand_cards: Player's hole cards
            community_cards: Community cards (optional)
            
        Returns:
            String description of hand strength
        """
        if not hand_cards:
            return "No cards"
        
        decoded_hand = self.decode_hand(hand_cards)
        cards = decoded_hand["cards"]
        
        # Basic hand strength analysis
        ranks = [card["rank"] for card in cards]
        suits = [card["suit"] for card in cards]
        
        # Check for pairs
        if len(set(ranks)) == 1:
            return f"Pocket {ranks[0]}s"
        
        # Check for suited cards
        if len(set(suits)) == 1:
            return f"Suited {ranks[0]}{ranks[1]}"
        
        # Check for connectors
        if abs(int(ranks[0]) - int(ranks[1])) == 1:
            return f"Connector {ranks[0]}{ranks[1]}"
        
        return f"{ranks[0]}{ranks[1]} offsuit"


def create_card_mapping() -> Dict[str, Dict[str, Union[str, int]]]:
    """
    Create a comprehensive mapping of all possible cards.
    
    Returns:
        Dictionary mapping card displays to full information
    """
    decoder = CardDecoder()
    card_mapping = {}
    
    for rank in range(13):
        for suit in [1, 2, 4, 8]:
            decoded = decoder.decode_card(rank, suit)
            card_mapping[decoded["display"]] = decoded
    
    return card_mapping


def format_card_for_display(card_data: Dict[str, int]) -> str:
    """
    Format a single card for display.
    
    Args:
        card_data: Card data with 'rank' and 'suit' keys
        
    Returns:
        Formatted card string
    """
    decoder = CardDecoder()
    decoded = decoder.decode_card(card_data["rank"], card_data["suit"])
    return decoded["pretty"]


def format_hand_for_display(hand_cards: List[Dict[str, int]]) -> str:
    """
    Format a player's hand for display.
    
    Args:
        hand_cards: List of hole cards
        
    Returns:
        Formatted hand string
    """
    decoder = CardDecoder()
    decoded_hand = decoder.decode_hand(hand_cards)
    return decoded_hand["pretty"]


def format_community_cards_for_display(community_cards: List[Dict[str, int]]) -> str:
    """
    Format community cards for display.
    
    Args:
        community_cards: List of community cards
        
    Returns:
        Formatted community cards string
    """
    decoder = CardDecoder()
    decoded_community = decoder.decode_community_cards(community_cards)
    return decoded_community["pretty"]


# Example usage and testing
if __name__ == "__main__":
    # Test the decoder
    decoder = CardDecoder()
    
    # Test single card
    test_card = {"rank": 11, "suit": 1}  # King of Spades
    result = decoder.decode_card(test_card["rank"], test_card["suit"])
    print(f"Test card: {result}")
    
    # Test hand
    test_hand = [
        {"rank": 11, "suit": 1},  # King of Spades
        {"rank": 10, "suit": 1}   # Queen of Spades
    ]
    hand_result = decoder.decode_hand(test_hand)
    print(f"Test hand: {hand_result}")
    
    # Test community cards
    test_community = [
        {"rank": 0, "suit": 2},   # 2 of Hearts
        {"rank": 1, "suit": 2},   # 3 of Hearts
        {"rank": 2, "suit": 2}   # 4 of Hearts
    ]
    community_result = decoder.decode_community_cards(test_community)
    print(f"Test community: {community_result}")
