# simple verilog path analyzer

A simple analyzer of Verilog/System Verilog code.
Intended to give a hint to find a critical path in the source.

## Requirements
PLY(Python Lex-Yacc) 3.11

## Example
```
> py svanalyzer.py sample.sv

loading the source file...
no dependency found on "msbcount1".

faddmc > modules

  priorityEncoder24_5
  faddmc

faddmc > shamt1   

  Direct dependency:
    exp_post1, calcbuf1, msbcount1, sig_pre1, sig_post1

  Upstream registers:
    exp_post1, sig_post1, calcbuf1, sig_pre1

faddmc > calcbuf1

  Direct dependency:
    op_pre0, exp_post0, exp_pre0, resetn, calcbuf0, sig_pre0, ret_sig0, sig_post0

  Upstream registers:
    op1, op2, resetn

faddmc > module priorityEncoder24_5


priorityEncoder24_5 > module faddmc


faddmc > flatten

  (ret) = (ret_sig1, ret_exp1, ret_manti1)
  (calcbuf0) = (sig_pre0, sig_post0, manti_pre, manti_post, manti_pre, manti_post)
  (ret_sig0) = (sig_pre0)
  (manti_post) = (op_post, expdiff)
  (manti_pre) = (op_pre0)
  (expdiff) = (exp_pre0, exp_post0)
  (exp_post0) = (op_post)
  (exp_pre0) = (op_pre0)
  (sig_post0) = (op_post)
  (sig_pre0) = (op_pre0)
  (premanti2) = (op2)
  ...
```

## Operations
+ *wirename*
  + list upstream wire/registers of *wirename*.
+ module *modulename*
  + move to *modulename*.
+ modules
  + list all modules in the source.
+ flatten
  + list direct dependencies of all wire/registers.
+ stats
  + show data of the module currently looking at.