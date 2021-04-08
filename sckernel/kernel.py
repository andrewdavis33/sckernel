from ipykernel.kernelbase import Kernel
from .sclangSub import *

class SCKernel(Kernel):
    implementation = "SuperCollider"
    implementation_version = "0.1"
    language = "SuperCollider"
    language_version = "3.10"
    language_info = {
        'name':'sclang',    
        'codemirror_mode':'sclang' # mode defined in kernel.js
    }
    banner = "SuperCollider Kernel"

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.sclangSubprocess = SclangSubprocess()

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        # silent should execute code but silence output - need to test 
        # especially with polling numbers, for example - not sure of
        # sclang behavior

        self.sclangSubprocess.send_code(code, silent)
        stream_content = {'name':'stdout', 'text':''}
        self.send_response(self.iopub_socket, 'stream', stream_content)

        return {
            'status': 'ok', 
            'execution_count':self.execution_count, 
            'payload': [], 
            'user_expressions': {}
        }
    
    def do_complete(self, code, cursor_pos):
        pass

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SCKernel)
