import tkinter as tk
from tkinter import scrolledtext
from tkinter import font
from tkinter import ttk
import sys
import threading
import queue

WINDOW_INTERVAL = 40 # Time in ms between screen refresh of text

def addToQueue(q):
    while True:
        try:
            line = sys.stdin.readline()
        except:
            q.put("") # Trigger quit from main thread
            break

        q.put(line)
        if line == "":
            break
    print("Exiting reader thread.")

def destroyWindow():
    root.destroy()
    print("Post window closed.")

def processText(q):
    quit = False
    try:
        while True:
            line = q.get_nowait()
            if line == "": quit = True
            textbox.insert(tk.END, line)
            textbox.see("end")
    except queue.Empty:
        if not quit:
            root.after(WINDOW_INTERVAL, processText, q)
        else:
            root.after(WINDOW_INTERVAL, destroyWindow)

def openingLine(q):
    textbox.insert(tk.END, "Post Window for SuperCollider:\n")
    root.after(WINDOW_INTERVAL, processText, q)

def zoomIn():
    font.configure(size=font.cget("size") + 2)

def zoomOut():
    font.configure(size=font.cget("size") - 2)

# Main code to run
q = queue.Queue()
t = threading.Thread(target=addToQueue, args=(q,))
t.daemon = True
root = tk.Tk()
root.geometry("600x500") # initial size but can be resizable
root.resizable(True, True)

# Font buttons
font = font.Font(family="Courier", size=14)
button_frame = tk.Frame(root)
button_frame.pack(fill="x")

# Top label and buttons
label=tk.Label(button_frame, text="SC Post Window")
zin = tk.Button(button_frame, text="Zoom In", command=zoomIn)
zout = tk.Button(button_frame, text="Zoom Out", command=zoomOut)
label.pack(side="left")
zin.pack(side="left")
zout.pack(side="left")

# Horizontal Separator
separator = ttk.Separator(root, orient="horizontal")
separator.pack(side="top", fill="x")

# Textbox
# Adding the width=1 and height=1 is necessary so that resizing font
# does not change the window size
textbox = scrolledtext.ScrolledText(root, width=1, height=1, font=font)
textbox.pack(expand=True, fill="both")
root.after(0, openingLine, q)

# Run display
print("Starting worker thread to process stdin and start main graphics loop...")
t.start()
root.mainloop()
print("Exiting...")
