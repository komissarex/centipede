from abc import ABCMeta, abstractmethod
from centipede import centipede
from  shutil import rmtree
import os
import threading
import commands
import subprocess
import psutil
import time

class BaseTester(threading.Thread):
    """
    Base abstract tester class, desined as thread
    """
    __metaclass__ =  ABCMeta

    def __init__(self, solution, semaphore):
        super(BaseTester, self).__init__()
        self.semaphore = semaphore
        self.solution = solution
        self.semaphore.acquire()

    def get_sandbox_path(self):
        """
        :return: Compilation and running folder
        """
        return os.path.join(centipede.config['SANDBOX_FOLDER'], str(self.solution.id))

    def get_compiled_file(self):
        """
        :return: Full path to the compiled file
        """
        return os.path.join(self.get_sandbox_path(), str(self.solution.id))

    def _compile_default(self, compilation_string):
        """
        Implements default compilation process
        :param compilation_string: Compilation string, containing {output} and {source} substrings
        :return: True, if compilation successful
        """
        self.solution.update(self.solution.STATUS['waiting']['compiling'])

        path = self.get_sandbox_path()
        if not os.path.exists(path):
            os.makedirs(path)

        status, output = commands.getstatusoutput(
            compilation_string\
            .format(output = self.get_compiled_file(), source = self.solution.get_solution_file()))

        if status != 0:
            self.solution.update(
                self.solution.STATUS['tested']['error']['ce'],
                message = output.decode('utf-8')
            )
            return False

        return True

    def _run_default(self, command = '{solution}'):
        """
        Implements default testing process
        :param command Running command, containing {solution} substring
        :return: True, if solution passed all tests
        """

        if self.compile():
            self.solution.update(self.solution.STATUS['waiting']['running'])

            test_number = 1
            memory_max = curr_time = 0
            for test in self.solution.problem.tests:
                # filling input
                input = open(os.path.join(self.get_sandbox_path(), 'input.txt'), 'w')
                input.write(str(test.input))
                input.close()

                # spawn solution file
                proc = subprocess.Popen(
                    command.format(solution = os.path.abspath(self.get_compiled_file())),
                    cwd = os.path.abspath(self.get_sandbox_path()),
                )

                # take care of time and memory
                start_time = time.time()
                while proc.poll() is None:
                    watchdog = psutil.Process(proc.pid)
                    curr_time = time.time() - start_time
                    memory = watchdog.get_memory_info().rss / 1024
                    if memory > memory_max:
                        memory_max = memory
                    print 'time: {time}, rss: {rss}'.format(time = curr_time, rss = memory)

                    # detectimg memory limit
                    if memory_max > self.solution.problem.memory * 1024:
                        proc.terminate()
                        self.solution.update(
                            self.solution.STATUS['tested']['error']['mle'],
                            time = curr_time,
                            memory = memory_max,
                            test_number = test_number
                        )
                        return False

                    # detecting time limit
                    if curr_time > self.solution.problem.time:
                        proc.terminate()
                        self.solution.update(
                            self.solution.STATUS['tested']['error']['tle'],
                            time = curr_time,
                            memory = memory_max,
                            test_number = test_number
                        )
                        return False

                # detecting crash
                if proc.returncode != 0:
                    self.solution.update(
                        self.solution.STATUS['tested']['error']['re'],
                        test_number = test_number
                    )
                    return False

                # catching presentation errors
                try:
                    output = open(os.path.join(self.get_sandbox_path(), 'output.txt'), 'r+')
                except IOError:
                    self.solution.update(
                        self.solution.STATUS['tested']['error']['pe'],
                        test_number = test_number
                    )
                    return False

                # catching WA
                if str(test.output).strip() != str(output.read()).strip():
                    self.solution.update(
                        self.solution.STATUS['tested']['error']['wa'],
                        test_number = test_number,
                        time = curr_time,
                        memory = memory_max
                    )
                    return False

                test_number += 1

            # all tests passed, hurrah!
            self.solution.update(
                self.solution.STATUS['tested']['accept'],
                time = curr_time,
                memory = memory_max
            )
            return True
        return False

    def __del__(self):
        self.semaphore.release()

    @abstractmethod
    def compile(self):
        """
        Compilation process
        """
        pass

    @abstractmethod
    def run(self):
        """
        Testing process
        """
        pass
