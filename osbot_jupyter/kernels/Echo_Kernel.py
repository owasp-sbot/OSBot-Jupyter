import json
import os

from IPython.utils.tempdir import TemporaryDirectory
from jupyter_client.kernelspec import KernelSpecManager
from pbx_gs_python_utils.utils.Dev import Dev
from pbx_gs_python_utils.utils.Files import Files


class Echo_Kernel:
    def __init__(self):
        self.kernel_name     = 'Echo'
        self.kernel_class    = self.__module__
        self.kernel_language = 'text'
        self.spec = {   "argv"        : ["python", "-m", self.kernel_class, "-f", "{connection_file}"],
                        "display_name": self.kernel_name    ,
                        "language"    : self.kernel_language,
                    }


    def install(self):
        with TemporaryDirectory() as td:
            os.chmod(td, 0o755) # check if this is needed
            with open(os.path.join(td, 'kernel.json'), 'w') as file:
                json.dump(self.spec, file, sort_keys=True)
            return KernelSpecManager().install_kernel_spec(td, 'echo', replace=True)

    def uninstall(self):
        return KernelSpecManager().remove_kernel_spec(self.kernel_name.lower())
