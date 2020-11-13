import threading
import _thread
import queue
import sys
import signal
import os
from subprocess import Popen, PIPE, DEVNULL

# TODO: Need to make sure there are no race conditions
# TODO: gracefully exiting if sclang not in path


class SclangSubprocess:
    # Constructor
    def __init__(self, input_prompt="sc3>", reply_prompt="->", encoding="utf-8"):
        # Signal handler for SIGINT
        # Log when process has seen the first shutdown call
        def sigint_handler(signum, frame):
            self.shutdown()
            sys.exit(0)
        self.shuttingDown = False
        signal.signal(signal.SIGINT, sigint_handler)
       
        # prompts and encoding
        self.input_prompt = input_prompt
        self.reply_prompt = reply_prompt
        self.encoding = encoding
        
        # Queue instance variables
        self.sclangToWindowQ = queue.Queue()
        
        # Subprocesses
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.window = Popen(
            ["python", os.path.join(dir_path, "window.py")], 
            stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, bufsize=0
        )

        self.sclang = Popen(
            ["sclang", "-i", "sckernel"], # IDE mode allows for no prompt text in stdout 
            stdin=PIPE, stdout=PIPE, stderr=DEVNULL, bufsize=0
        )

        # Worker thread to process sclang output and window input
        self.receiverStdout = threading.Thread(
            target=self.__receive_output, 
            args=(self.sclang.stdout,)
        )
        self.processor = threading.Thread(target=self.__process_output)

        # Start threads
        self.receiverStdout.start()
        self.processor.start()

    # Private methods
    def __receive_output(self, fd):
        while True:
            outputLine = fd.readline() # blocks, no timeout
            if not outputLine: break
            outputLine = outputLine.decode(self.encoding)
            self.sclangToWindowQ.put(outputLine)
        
        # Indicate to window thread that there is no more output
        self.sclangToWindowQ.put(None)
        
        # interrupt main thread which needs to catch signal.SIGINT
        if not self.shuttingDown: os.kill(os.getpid(), signal.SIGINT)

    def __sendToWindow(self, line):
        lineWithNewline = line + '\n'
        self.window.stdin.write(lineWithNewline.encode(self.encoding))

    def __getLine(self):
        line = self.sclangToWindowQ.get() # blocks, no timeout
        self.sclangToWindowQ.task_done()
        if line == None: return None
        return line.rstrip()

    def __process_output(self):
        while True:
            line = self.__getLine()
 
            if line == None: break
            else: 
                self.__sendToWindow(line)        
    
    # Public methods
    def send_code(self, code, silent = False):
        if code == '': return False, code
        
        code += '\n'

        # attempted to write to sclang, otherwise
        # report that sclang has been shutdown
        try:
            self.sclang.stdin.write(code.encode())

            if silent:
                self.sclang.stdin.write(bytearray.fromhex("1b"))
            else:
                self.sclang.stdin.write(bytearray.fromhex("0c"))
            return True
        except IOError:
            return False



    def shutdown(self):
        self.shuttingDown = True

        print()
        print("Closing input to sclang stdin and waiting for" +
        "worker thread to finish consuming sclang stdout...")
        self.sclang.stdin.close()
        self.receiverStdout.join()
        print("sclang stdout consumed and consumer thread joined.")

        print()
        print("Waiting for all output to be sent to window...")
        self.sclangToWindowQ.join()
        self.window.stdin.close()
        print("All output sent to window.")

        print()
        print("Waiting for window subprocess to close and" +
        " processor thread to join...")
        self.processor.join()
        self.window.wait()
        print("Window subprocess closed and processor thread joined.")
        print("Exiting...")

if __name__ == "__main__":
    sclang = SclangSubprocess()

    while True:
        code = input("sc3> ")
        sclang.send_code(code)

    sclang.shutdown()
