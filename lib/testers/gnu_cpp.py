# -*- coding: utf-8 -*-
from base_tester import BaseTester

class Tester(BaseTester):
    """
    GNU C++ Tester
    """

    def compile(self):
        return self._compile_default('g++ -o {output} {source}')

    def run(self):
        return self._run_default()

