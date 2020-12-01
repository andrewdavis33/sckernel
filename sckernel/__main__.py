from ipykernel.kernelapp import IPKernelApp
from . import SCKernel

IPKernelApp.launch_instance(kernel_class=SCKernel)
