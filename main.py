import os
import sys
from graph import graph
from formatter import OutputFormatter

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Meeting Summary Agent")
    print("=" * 60)

    user_input = input("How can I help you today? (type 'exit' to quit): ").strip()

    if not user_input or user_input.lower() == "exit":
        sys.exit("No input provided. Exiting...")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    transcript_file = os.path.join(script_dir, "transcript.txt")

    transcript = ""
    if os.path.exists(transcript_file):
        with open(transcript_file, "r", encoding="utf-8") as fh:
            transcript = fh.read().strip()
        print("Loaded transcript.\n")
    else:
        print("Warning: transcript.txt not found.\n")

    final = graph.invoke({ "user_input": user_input, "transcript": transcript })
    OutputFormatter.format_output(final["final_response"])