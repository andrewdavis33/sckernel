import threading
import _thread
import queue
import sys
import signal
import os
from subprocess import Popen, PIPE, DEVNULL
import subprocess
import time

class SclangSubprocess:
    def __init__(self, encoding="utf-8"):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        window_path = os.path.join(dir_path, "window.py")
        if not os.path.exists(window_path):
            raise("window.py is not in the same directory as" +
            "sclangSub.py")

        self.encoding = encoding
        self.window_queue = queue.Queue()

        try: 
            self.window = Popen(
                ["python", window_path], 
                stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, bufsize=0
            )
        except:
            raise RuntimeError("Could not open window.py.  Make sure"
            + " that 'python' is in $PATH.")

        try:
            self.sclang = Popen(
                # IDE mode suppresses sc3> prompt text and input
                ["sclang", "-i", "sckernel"],
                stdin=PIPE, stdout=PIPE, stderr=DEVNULL, bufsize=0
            )
        except:
            self.window.kill()
            self.window.wait()
            raise RuntimeError("Could not open sclang.  Check to make "
            + "sure sclang is in $PATH")

        self.receiver = threading.Thread(target=self.__receive_output)
        self.receiver.daemon = True
        self.processor = threading.Thread(target=self.__process_output)
        self.processor.daemon = True
        self.receiver.start()
        self.processor.start() 

        self.shuttingDown = False
        self.lock = threading.RLock()
        
        def sig_handler(signum, frame):
            self.shutdown() 
        
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)

    def __receive_output(self):
        while True:
            try:
                outputLine = self.sclang.stdout.readline()
            except:
                break
            if not outputLine: break
            outputLine = outputLine.decode(self.encoding)
            self.window_queue.put(outputLine)
        
        # Tell window loop to stop processing
        self.window_queue.put(None)

    def __sendToWindow(self, line):
        try:
            self.window.stdin.write(line.encode(self.encoding))
        except:
            # Do not quit process because we may still be
            # able to read and write from sclang.
            print("Cannot write to window.py. Continuing execution.")

    def __process_output(self):
        while True:
            line = self.window_queue.get()
 
            if line is None: break
            else: 
                self.__sendToWindow(line)

        self.window.stdin.close() 
        
        self.lock.acquire()
        if not self.shuttingDown:
            self.shuttingDown = True
            self.lock.release()

            # sclang interpreter must have terminated
            print()
            print("sclang interpeter shutdown. Exiting "
            "from worker thread.")
            self.sclang.wait()
            print("sclang shutdown")
            self.window.wait()
            os._exit(1)
        else:
            pass # let shutdown happen from main thread
 
    def get_code(self):
        try:
            code = input("sc3> ")
            error = self.send_code(code)
            if error: self.shutdown()
        except EOFError:
            self.shutdown()

    def send_code(self, code, silent = False):
        if code == '': return False, code
        
        code += '\n'

        # attempted to write to sclang, otherwise
        # report that sclang has been shutdown
        try:
            self.sclang.stdin.write(code.encode(self.encoding))
            if silent:
                self.sclang.stdin.write(bytearray.fromhex("1b"))
            else:
                self.sclang.stdin.write(bytearray.fromhex("0c"))
            return False
        except IOError:
            print("Could not write to stdin of sclang.")
            return True
        except:
            print("Some issue other than an IOError when writing to "
            + "stdin of sclang")
            return True

    def shutdown(self):
        self.lock.acquire()
        if not self.shuttingDown:
            self.shuttingDown = True
            self.lock.release()        

            print("Shutting down...")
            print("Closing input to sclang stdin and waiting for" +
            " subprocesses to close.")
            self.sclang.stdin.close()
            self.sclang.wait()
            print("Sclang subprocess closed.")
            self.window.wait()
            print("Window subprocess closed.")
            print("Exiting...")
            sys.exit(0)
 
if __name__ == "__main__":
    sclang = SclangSubprocess()

    while True:
        sclang.get_code()
