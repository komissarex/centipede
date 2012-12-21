# -*- coding: utf-8 -*-
from base_tester import BaseTester

class Tester(BaseTester):
    """
    Free Pascal Tester
    """

    def compile(self):
        return self._compile_default('fpc -So -XS {source} -o{output}')

    def run(self):
        return self._run_default()

