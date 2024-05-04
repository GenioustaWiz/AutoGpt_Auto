import os
import openai
import tkinter as tk
from tkinter import messagebox, filedialog

# Install required packages
# pip install openai
# !pip install tk

# Initialize the Tkinter window
window = tk.Tk()
window.geometry("400x500")
window.title("AutoGPT App")

# Initialize the API key entry field
api_key_label = tk.Label(window, text="OpenAI API Key:")
api_key_label.pack()
api_key_entry = tk.Entry(window)
api_key_entry.pack()

# Save the API key to the computer environmental variables
def save_key():
    key = api_key_entry.get().strip()
    if key:
        os.environ["AUTOGPT_API_KEY"] = key
        messagebox.showinfo("API Key Saved", "API Key saved successfully!")
        window.destroy()
    else:
        messagebox.showerror("Error", "Please enter a valid API Key.")

save_key_button = tk.Button(window, text="Save API Key", command=save_key)
save_key_button.pack()

# Check if the API key is already present in the environmental variables
if "AUTOGPT_API_KEY" in os.environ:
    api_key_entry.insert(0, os.environ["AUTOGPT_API_KEY"])
    save_key_button.destroy()

    # Initialize the prompts entry field
    prompts_label = tk.Label(window, text="Prompts:")
    prompts_label.pack()
    prompts_entry = tk.Entry(window)
    prompts_entry.pack()

    # Initialize the goals entry fields
    goals = []

    def add_goal():
        goal_entry = tk.Entry(window)
        goal_entry.pack()
        goals.append(goal_entry)

    add_goal_button = tk.Button(window, text="Add Goal", command=add_goal)
    add_goal_button.pack()

    # Initialize the generate output button
    def generate_output():
        prompt = prompts_entry.get().strip()
        if prompt:
            goal_text = ""
            for goal in goals:
                goal_text += "- " + goal.get().strip() + "\n"
            if goal_text:
                prompt += "\n\nGoals:\n" + goal_text

            # Generate the output from OpenAI GPT
            openai.api_key = os.environ["AUTOGPT_API_KEY"]
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            output = response.choices[0].text.strip()

            # Display the output to the user
            output_label.config(text=output)

        else:
            messagebox.showerror("Error", "Please enter a prompt.")

    generate_output_button = tk.Button(window, text="Generate Output", command=generate_output)
    generate_output_button.pack()

    # Initialize the output display field
    output_label = tk.Label(window, text="")
    output_label.pack()

    # Initialize the save results button
    def save_results():
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, "w") as file:
                file.write(prompts_entry.get().strip() + "\n\n")
                for goal in goals:
                    file.write("- " + goal.get().strip() + "\n")
                file.write("\n" + output_label.cget("text"))

    save_results_button = tk.Button(window, text="Save Results", command=save_results)
    save_results_button.pack()

window.mainloop()
