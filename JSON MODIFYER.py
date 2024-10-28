import json
import os

def load_qa_pairs(filename):
    """Load Q&A pairs from the specified JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error: The JSON file is not valid. Please check the format. Details: {e}")
                return {}
    else:
        print(f"File '{filename}' not found.")
        return {}

def save_qa_pairs(filename, qa_pairs):
    """Save the Q&A pairs to the specified JSON file."""
    with open(filename, 'w') as file:
        json.dump(qa_pairs, file, indent=4)
        print(f"Successfully saved Q&A pairs to '{filename}'.")

def display_qa_pairs(qa_pairs):
    """Display the Q&A pairs."""
    if qa_pairs:
        print("\nCurrent Q&A Pairs:")
        for question, answer in qa_pairs.items():
            print(f"Q: {question}\nA: {answer}\n")
    else:
        print("No Q&A pairs found.")

def fix_json(filename, lowercase=False):
    """Attempt to fix common JSON issues and optionally lowercase all letters."""
    with open(filename, 'r') as file:
        content = file.read()

    # Attempt to fix common JSON issues (this is a basic fix)
    content = content.replace(",}", "}").replace(",]", "]")  # Remove trailing commas
    content = content.replace("}{", "},{")  # Ensure objects are separated properly

    # Try to load the fixed content
    try:
        fixed_qa_pairs = json.loads(content)
        if lowercase:
            # Lowercase all keys and values
            fixed_qa_pairs = {k.lower(): v.lower() for k, v in fixed_qa_pairs.items()}

        with open(filename, 'w') as file:
            json.dump(fixed_qa_pairs, file, indent=4)
        print(f"Successfully fixed and saved the JSON file '{filename}'.")
    except json.JSONDecodeError as e:
        print(f"Failed to fix the JSON file. Please check it manually. Details: {e}")

def main():
    filename = "qa_pairs.json"
    
    # Load existing Q&A pairs
    qa_pairs = load_qa_pairs(filename)
    display_qa_pairs(qa_pairs)

    while True:
        action = input("Would you like to (a)dd, (e)dit, (d)elete, (f)ix the JSON or (q)uit? ").lower()

        if action == 'a':
            question = input("Enter the question: ")
            answer = input("Enter the answer: ")
            qa_pairs[question] = answer
            print(f"Added: Q: {question} A: {answer}")

        elif action == 'e':
            question = input("Enter the question to edit: ")
            if question in qa_pairs:
                new_answer = input("Enter the new answer: ")
                qa_pairs[question] = new_answer
                print(f"Updated: Q: {question} A: {new_answer}")
            else:
                print("Question not found.")

        elif action == 'd':
            question = input("Enter the question to delete: ")
            if question in qa_pairs:
                del qa_pairs[question]
                print(f"Deleted question: {question}")
            else:
                print("Question not found.")

        elif action == 'f':
            lowercase = input("Would you like to lowercase all letters? (y/n): ").lower() == 'y'
            fix_json(filename, lowercase)
            qa_pairs = load_qa_pairs(filename)  # Reload to see fixed Q&A pairs
            display_qa_pairs(qa_pairs)

        elif action == 'q':
            break

        else:
            print("Invalid option. Please try again.")

        # Save updated Q&A pairs back to the JSON file
        save_qa_pairs(filename, qa_pairs)

if __name__ == "__main__":
    main()

