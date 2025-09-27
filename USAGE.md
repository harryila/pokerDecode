# Usage Guide

## Quick Start

1. **Run the decoder on simulation data:**
   ```bash
   python run_decoder.py path/to/simulation_data
   ```

2. **Use in Python code:**
   ```python
   from simple_poker_decoder import SimplePokerDecoder
   
   decoder = SimplePokerDecoder()
   decoder.decode_simulation("path/to/simulation_data")
   ```

## Expected Simulation Structure

The decoder expects simulation data in this structure:
```
simulation_data/
├── simulation_meta.json
├── game_logs/
│   ├── hand_1_PREFLOP_player_0_raise.json
│   ├── hand_1_PREFLOP_player_1_call.json
│   └── ...
├── chat_logs/
│   ├── hand_1_msg_1_0.json
│   └── ...
└── chat_dataset/
    ├── conversations.json
    └── game_contexts.json
```

## Output

The decoder creates a text file with human-readable poker game data in this format:

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
