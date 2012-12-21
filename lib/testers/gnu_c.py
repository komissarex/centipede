# -*- coding: utf-8 -*-
from base_tester import BaseTester

class Tester(BaseTester):
    """
    GNU C Tester
    """

    def compile(self):
        return self._compile_default('gcc -std=c99 -o {output} {source}')

    def run(self):
        return self._run_default()

