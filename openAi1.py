import os
import openai
import tkinter as tk
from tkinter import messagebox, filedialog

# Install packages
# os.system('pip install autogpt')
# os.system('pip install tkinter')

# Initialize the tkinter app
app = tk.Tk()
app.title("AutoGPT App")


# Define functions
def save_api_key():
    """Saves the OpenAI API key to the computer environmental variables"""
    api_key = api_key_entry.get()
    if api_key:
        os.environ['AUTOGPT_API_KEY'] = api_key
        messagebox.showinfo("AutoGPT App", "API key saved successfully.")
        save_key_button.destroy()
    else:
        messagebox.showerror("AutoGPT App", "Please enter an API key.")

def add_goal():
    """Adds a new entry for user's goals"""
    global goal_entries
    goal_entries.append(tk.Entry(frame, width=50))
    goal_entries[-1].grid(row=len(goal_entries)+2, column=0)

# def generate_output():
#     """Generates output from AutoGPT based on the user's prompts"""
#     global prompts_entry, output_text
#     prompts = prompts_entry.get()
#     if not prompts:
#         messagebox.showerror("AutoGPT App", "Please enter prompts.")
#         return
#     try:
#         openai.api_key = os.environ['AUTOGPT_API_KEY']
#     except KeyError:
#         messagebox.showerror("AutoGPT App", "API key not found. Please save API key first.")
#         return
#     output_text.delete("1.0", tk.END)
#     for i in range(len(goal_entries)):
#         goal = goal_entries[i].get()
#         if goal:
#             output = openai.Completion.create(engine="davinci", prompt=prompts+goal, max_tokens=2048)
#             output_text.insert(tk.END, f"Goal {i+1}: {goal}\n\n{output.choices[0].text}\n\n")
#     save_button.config(state="normal")

def generate_output():
    """Generates output from AutoGPT based on the user's prompts"""
    global prompts_entry, output_text
    prompts = prompts_entry.get()
    if not prompts:
        messagebox.showerror("AutoGPT App", "Please enter prompts.")
        return
    try:
        openai.api_key = os.environ['AUTOGPT_API_KEY']
        output_text.delete("1.0", tk.END)
        for i in range(len(goal_entries)):
            goal = goal_entries[i].get()
            if goal:
                output = openai.Completion.create(engine="davinci", prompt=prompts+goal, max_tokens=2048)
                output_text.insert(tk.END, f"Goal {i+1}: {goal}\n\n{output.choices[0].text}\n\n")
        save_button.config(state="normal")
    except openai.error.RateLimitError:
        messagebox.showerror("AutoGPT App", "You have exceeded your API usage quota. Please check your OpenAI account or upgrade your plan.")
    except Exception as e:
        messagebox.showerror("AutoGPT App", f"Error generating output: {str(e)}")


def save_results():
    """Saves the prompts and output generated from AutoGPT to a file"""
    global prompts_entry, output_text
    prompts = prompts_entry.get()
    if not prompts:
        messagebox.showerror("AutoGPT App", "Please enter prompts.")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("PDF files", "*.pdf")])
    if filename:
        with open(filename, "w") as f:
            f.write(prompts + "\n\n" + output_text.get("1.0", tk.END))

# Check if API key is available
if 'AUTOGPT_API_KEY' in os.environ:
    api_key = os.environ['AUTOGPT_API_KEY']
else:
    api_key = ""
    save_key_button = tk.Button(app, text="Save Key", command=save_api_key)
    save_key_button.pack(side="top")
    save_button = tk.Button(app, text="Save Results", command=save_results, state="disabled")
    save_button.pack(side="bottom")

# Create the UI elements
api_key_label = tk.Label(app, text="OpenAI API Key:")
api_key_label.pack(side="top")
api_key_entry = tk.Entry(app, width=50)
api_key_entry.pack(side="top")
api_key_entry.insert(tk.END, api_key)

prompts_label = tk.Label(app, text="Enter prompts:")
prompts_label.pack(side="top")
prompts_entry = tk.Entry(app, width=50)
prompts_entry.pack(side="top")

goal_label = tk.Label(app, text="Enter goals:")
goal_label.pack(side="top")
frame = tk.Frame(app)
frame.pack(side="top")
goal_entries = [tk.Entry(frame,width=50)]
goal_entries[0].grid(row=0, column=0)
add_button = tk.Button(app, text="Add goal", command=add_goal)
add_button.pack(side="top")

output_label = tk.Label(app, text="Output:")
output_label.pack(side="top")
output_text = tk.Text(app, height=10)
output_text.pack(side="top")

generate_button = tk.Button(app, text="Generate output", command=generate_output)
generate_button.pack(side="top")

if 'AUTOGPT_API_KEY' in os.environ:
    generate_button.focus_set()
else:
    api_key_entry.focus_set()
    save_button.focus_set()

app.mainloop()

