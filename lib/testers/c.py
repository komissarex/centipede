from abstract_tester import AbstractTester
import commands, os

class CTester(AbstractTester):
    """
    GNU C Tester
    """

    def compile(self):
        self.solution.update_status(self.solution.STATUS['waiting']['compiling'])
        path = self.get_compilation_path()
        if not os.path.exists(path):
            os.makedirs(path)
        status, output = commands.getstatusoutput(
            'gcc -static -fno-optimize-sibling-calls -fno-strict-aliasing -fno-asm -lm -s -O2 -o %s %s' %
            (self.get_compiled_file(), self.solution.get_solution_file()))

        if status != 0:
            self.solution.update_status(self.solution.STATUS['error']['ce'])
            self.solution.update_message(output)
            return False
        else:
            return True

    def run(self):
        if self.compile():
            self.solution.update_status(self.solution.STATUS['waiting']['running'])
            print(self.solution.problem.tests)
            for test in self.solution.problem.tests:
                input = open(os.path.join(self.get_compilation_path(), 'input.txt'), 'w+')
                input.write(test.input)
                os.spawnvpe(os.P_WAIT, self.get_compiled_file(), [], {'PWD': self.get_compilation_path()})
                output = open(os.path.join(self.get_compilation_path(), 'output.txt'), 'w+')

                if input.read().strip() != output.read().strip():
                    self.solution.update_status(self.solution.STATUS['error']['wa'])
                    return False
            self.solution.update_status(self.solution.STATUS['accept'])
            return True

