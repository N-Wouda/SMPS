# SMPS
[![Build Status](https://travis-ci.com/N-Wouda/SMPS.svg?branch=master)](https://travis-ci.com/N-Wouda/SMPS)
[![codecov](https://codecov.io/gh/N-Wouda/SMPS/branch/master/graph/badge.svg)](https://codecov.io/gh/N-Wouda/SMPS)

This repository provides a Python package for parsing stochastic programming 
problems in the SMPS format.

TODO user manual/documentation

TODO pip install

## Motivation

To the best of my knowledge, there are two projects for parsing SMPS files in 
Python:

- [`pysmps`](https://github.com/jmaerte/pysmps), which parses (S)MPS
  problems with stochasticity defined in BLOCK or INDEP form. SCENARIOS are not
  supported, nor are distributions.
- [`smps`](https://github.com/robin-vjc/smps), which does not handle BLOCK and 
  INDEP stochasticity, (linear) transformations, nor distributions.

These projects are both limited in scope, as they exclude a large number of 
acceptable SMPS formulations. Furthermore, there exists no project that
correctly parses distributions (i.e., non-discrete SMPS specifications). A 
Python infrastructure for stochastic programming requires full support for
parsing SMPS files, which the existing projects do not provide.

## How to use

TODO

## How to develop

TODO

## Cite

In case you have used this package in a published work, please consider citing it as

> Wouda, N.A. 2020. A Python package for parsing stochastic programming problems
> in the SMPS format. https://github.com/N-Wouda/SMPS.

## References

TODO

