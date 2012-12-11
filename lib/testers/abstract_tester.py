from abc import ABCMeta, abstractmethod
from centipede import centipede
import os, threading

class AbstractTester(threading.Thread):
    """
    Abstract tester class, desined as thread
    """
    __metaclass__ =  ABCMeta

    def __init__(self, solution):
        super(AbstractTester, self).__init__()
        self.solution = solution

    def get_compilation_path(self):
        """
        :return: Compilation folder
        """
        return os.path.join(centipede.config['SANDBOX_FOLDER'], str(self.solution.id))

    def get_compiled_file(self):
        """
        :return: Full path to the compiled file
        """
        return os.path.join(self.get_compilation_path(), str(self.solution.id))

    @abstractmethod
    def compile(self):
        """
        Compilation
        """
        pass

    @abstractmethod
    def run(self):
        """
        Test, test, test!..
        """
        pass
