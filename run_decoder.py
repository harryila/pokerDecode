#!/usr/bin/env python3
"""
Simple script to run the poker decoder on simulation data.

Usage:
    python run_decoder.py path/to/simulation_data
"""

import sys
import os
from simple_poker_decoder import SimplePokerDecoder


def main():
    """Main function to run the decoder."""
    if len(sys.argv) != 2:
        print("Usage: python run_decoder.py path/to/simulation_data")
        print("Example: python run_decoder.py data/simulation_1")
        sys.exit(1)
    
    simulation_path = sys.argv[1]
    
    if not os.path.exists(simulation_path):
        print(f"Error: Simulation path not found: {simulation_path}")
        sys.exit(1)
    
    # Initialize decoder
    decoder = SimplePokerDecoder()
    
    try:
        # Decode the simulation
        output_file = decoder.decode_simulation(simulation_path)
        print(f"Decoded simulation saved to: {output_file}")
        
        # Show preview
        print("\n--- PREVIEW ---")
        with open(output_file, 'r') as f:
            preview = f.read()[:1000]
            print(preview)
            if len(preview) == 1000:
                print("... (truncated)")
        
    except Exception as e:
        print(f"Error processing simulation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
