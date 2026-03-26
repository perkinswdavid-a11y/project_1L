from pathlib import Path
from src.project_1l.data_layer.multi_streamer import MultiInstrumentStreamer

# Configuration
DB_PATH = Path(r"E:\project_1L\marketdata\catalog\marketdata.duckdb")
target_date = "20230711"
output_file = "ilh_sample_extract_20230711.csv"

def export_sample_data():
    streamer = MultiInstrumentStreamer(DB_PATH)
    
    print(f"Generating sample extract for {target_date} (08:30 - 09:30)...")
    
    # Use the MultiInstrumentStreamer to get the synchronized data
    # Note: I'll handle the time filtering in this export script specifically
    df = streamer.get_merged_stream(target_date, ["MES.v.0", "MNQ.v.0"])
    
    # Filter for the first hour of RTH
    start_time = f"2023-07-11 08:30:00"
    end_time = f"2023-07-11 09:30:00"
    
    # Convert ts_event to string for easy comparison if needed, 
    # but pandas handles datetime filtering well
    sample_df = df[(df['ts_event'] >= start_time) & (df['ts_event'] <= end_time)]
    
    # Limit to first 10,000 events to keep the file size reasonable for a friend's first look
    sample_df = sample_df.head(10000)
    
    # Save to CSV
    sample_df.to_csv(output_file, index=False)
    print(f"Successfully exported {len(sample_df)} events to {output_file}")

if __name__ == "__main__":
    export_sample_data()
