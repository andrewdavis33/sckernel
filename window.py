import tkinter as tk
from tkinter import scrolledtext
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

# Main code to run
q = queue.Queue()
t = threading.Thread(target=addToQueue, args=(q,))
t.daemon = True
root = tk.Tk()
root.resizable(True, True)
textbox = scrolledtext.ScrolledText(root)
textbox.pack()
root.after(0, openingLine, q)

# Run display
print("Starting worker thread to process stdin and start main graphics loop...")
t.start()
root.mainloop()
print("Exiting...")
