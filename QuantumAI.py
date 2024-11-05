import customtkinter as ctk
import json
import os
import platform

import platform

if platform.system() != "Linux":
    print("Not running on Linux.")
else:
    print("Running on Linux - executing code...")
    

# Function to load Q&A pairs from JSON file
def load_qa_pairs(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                qa_pairs = json.load(file)
                # Ensure all keys are in lowercase for case-insensitive matching
                return {key.lower(): value for key, value in qa_pairs.items()}
            except json.JSONDecodeError as e:
                print(f"Error loading JSON: {e}")
                return {}
    else:
        print(f"File '{filename}' does not exist.")
        return {}

# User display name
user = "User: "

class ChatBotApp:
    def __init__(self, master):
        self.master = master
        master.title("Quantum AI")

        # Load Q&A pairs from JSON
        self.qa_pairs = load_qa_pairs("qa_pairs.json")

        # Log the loaded Q&A pairs to ensure they are loaded correctly
        print("Loaded Q&A pairs:", self.qa_pairs)

        # Chat display frame
        self.chat_frame = ctk.CTkFrame(master)
        self.chat_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")  # Sticky for resizing

        self.scrollbar = ctk.CTkScrollbar(self.chat_frame)
        self.scrollbar.pack(side=ctk.RIGHT, fill=ctk.Y)

        self.chat_text = ctk.CTkTextbox(self.chat_frame, wrap=ctk.WORD, state=ctk.DISABLED)
        self.chat_text.pack(expand=True, fill=ctk.BOTH)
        self.scrollbar.configure(command=self.chat_text.yview)

        # User input frame
        self.input_frame = ctk.CTkFrame(master)
        self.input_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")  # Sticky for resizing

        self.input_label = ctk.CTkLabel(self.input_frame, text=user)
        self.input_label.pack(side=ctk.LEFT)

        self.input_entry = ctk.CTkEntry(self.input_frame, width=50)
        self.input_entry.pack(side=ctk.LEFT, expand=True, fill=ctk.X)  # Expand to fill available space

        self.send_button = ctk.CTkButton(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=ctk.LEFT)

        # Configure grid weights for resizing
        master.grid_rowconfigure(0, weight=1)  # Allow chat frame to expand
        master.grid_rowconfigure(1, weight=0)  # Keep input frame height fixed
        master.grid_columnconfigure(0, weight=1)  # Allow the column to expand

    def send_message(self):
        user_input = self.input_entry.get().strip()  # Get and strip input
        self.display_message(f"{user}: {user_input}")

        if user_input.startswith("python "):
            command = user_input[len("python "):]
            try:
                exec_globals = {}
                exec(command, exec_globals)
                result = exec_globals.get('result', 'Command executed')
                self.display_message(f"Quantum AI: {result}")
            except Exception as e:
                self.display_message(f"Quantum AI: Error: {e}")
        else:
            response = self.qa_pairs.get(user_input.lower(), "Quantum AI: Sorry, I don't understand that question.")
            self.display_message(response)

        self.input_entry.delete(0, ctk.END)  # Clear input field

    def display_message(self, message):
        self.chat_text.configure(state=ctk.NORMAL)
        self.chat_text.insert(ctk.END, message + "\n")
        self.chat_text.configure(state=ctk.DISABLED)
        self.chat_text.see(ctk.END)  # Auto-scroll to the bottom

def main():
    ctk.set_appearance_mode("dark")  # Set to "dark" or "light"
    ctk.set_default_color_theme("blue")  # Change to your desired theme color

    root = ctk.CTk()
    root.geometry("800x600")  # Set window size to 800x600
    app = ChatBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
