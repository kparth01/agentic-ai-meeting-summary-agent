import os
import sys
from graph import app
from formatter import OutputFormatter

if __name__ == "__main__":
    print("\n" * 1)
    print("=" * 60)
    print("Meeting summary agent")
    print("=" * 60)

    user_input = input("How can I help you today? (type 'exit' to quit): ").strip()
    transcript = ""

    if not user_input or user_input.lower() == "exit":
        (sys.exit("No input provided. Exiting the program..."))

    # /Users/parthkansara/Projects/AITrainingsNisarg/AgenticAIProjects/LangGraphPOC/transcript.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    transcript_file = os.path.join(script_dir, "transcript.txt")
    if os.path.exists(transcript_file):
        with open(transcript_file, "r", encoding="utf-8") as fh:
            transcript = fh.read().strip()
        print("Loaded transcript")

    result = app.invoke({"user_input": user_input, "transcript": transcript})
    OutputFormatter.format_output(result["combine"])