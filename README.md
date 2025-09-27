# Poker Game Decoder

Decodes poker simulation data into human-readable format for verification.

## Usage

```python
from simple_poker_decoder import SimplePokerDecoder

# Initialize decoder
decoder = SimplePokerDecoder()

# Decode a simulation
decoder.decode_simulation("path/to/simulation_data")
```

## Output Format

```
Hand 1 - preflop:
player0: K of Spades (K♠), Q of Hearts (Q♥) & [has 490 chips left]
player1: 2 of Hearts (2♥), 3 of Hearts (3♥) & [has 485 chips left]
board: No community cards
BB: player1
SB: player0
Actions:
player0: "I'm feeling lucky today!" & raised 10
player1: "Nice hand!" & called 10
```

## Files

- `simple_poker_decoder.py` - Main decoder
- `simple_game_display.py` - Display logic
- `card_utils.py` - Card decoding utilities
- `simulation_processor.py` - Simulation data processing