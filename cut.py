from pydub import AudioSegment

def cut_mp3_segment(input_file, output_file, start_time_sec, end_time_sec):
    """
    Cuts a segment from an MP3 file and saves it as a new MP3.

    Args:
        input_file (str): Path to the input MP3 file.
        output_file (str): Path to save the output MP3 file.
        start_time_sec (float): Start time of the segment in seconds.
        end_time_sec (float): End time of the segment in seconds.
    """
    try:
        song = AudioSegment.from_mp3(input_file)

        start_time_ms = start_time_sec * 1000
        end_time_ms = end_time_sec * 1000

        cut_segment = song[start_time_ms:end_time_ms]
        cut_segment.export(output_file, format="mp3")
        print(f"Segment successfully saved to {output_file}")
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
input_mp3 = "D:/завантажено/siames.mp3"  # Replace with your input file path
output_mp3 = "D:/завантажено/newaudio.mp3" # Replace with your desired output path
start = 27.0  # Start cutting at 15 seconds
end = 75.0    # End cutting at 45 seconds

cut_mp3_segment(input_mp3, output_mp3, start, end)