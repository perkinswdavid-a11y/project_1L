
import re
from datetime import datetime

def analyze_excursions(log_file):
    with open(log_file, 'r') as f:
        content = f.read()

    # Pattern to find TIME_STOP exits and their PnL
    # [2023-07-13 10:54:56.537726-05:00] LONG TIME_STOP @ 4529.25 | PnL: $-17.50
    time_stop_pattern = r"\[(.*?)\] (LONG|SHORT) TIME_STOP @ ([\d.]+) \| PnL: \$([-]?[\d.]+)"
    time_stops = re.findall(time_stop_pattern, content)

    total_time_stops = len(time_stops)
    negative_pnl_time_stops = [float(p) for _, _, _, p in time_stops if float(p) < 0]
    total_loss_from_time_stops = sum(negative_pnl_time_stops)

    print(f"--- Diagnostic Report: Time-Stop Analysis ---")
    print(f"Total Time-Stops: {total_time_stops}")
    print(f"Total Losses from Time-Stops: ${total_loss_from_time_stops:.2f}")
    if total_time_stops > 0:
        print(f"Average Loss per Time-Stop: ${total_loss_from_time_stops / total_time_stops:.2f}")
    
    # Check for trades that were "saved" or "killed"
    # This script is a simple parser, but it shows the scale of the bleed.
    
    # Check for Surge distribution
    surge_pattern = r"Signal Generated: .*? \| Surge: ([-]?\d+)"
    surges = [int(s) for s in re.findall(surge_pattern, content)]
    
    low_surges = [s for s in surges if abs(s) < 300]
    high_surges = [s for s in surges if abs(s) >= 300]
    
    print(f"\n--- Signal Distribution ---")
    print(f"Total Signals: {len(surges)}")
    print(f"Low Quality (<300 Surge): {len(low_surges)} ({len(low_surges)/len(surges)*100:.1f}%)" if surges else "No signals")
    print(f"High Quality (>=300 Surge): {len(high_surges)} ({len(high_surges)/len(surges)*100:.1f}%)" if surges else "No signals")

if __name__ == "__main__":
    analyze_excursions("full_test_output.txt")
