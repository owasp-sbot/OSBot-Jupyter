import json
import os


from jupyter_client.kernelspec import KernelSpecManager
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files

from osbot_jupyter.api.Kernel_Install import Kernel_Install


class Echo_Kernel:
    def __init__(self):
        self.kernel_name     = 'Echo'
        self.kernel_class    = self.__module__
        self.kernel_language = 'text'
        self.spec = {   "argv"        : ["python", "-m", self.kernel_class, "-f", "{connection_file}"],
                        "display_name": self.kernel_name    ,
                        "language"    : self.kernel_language,
                    }

    #def exists(self):
    #    return self.kernel_install.current_kernels()


