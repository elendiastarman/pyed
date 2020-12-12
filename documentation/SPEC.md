# Pyed Specification

The primary building blocks of Pyed are `PyedNode`, which represents a set of instructions to execute, and `PyedValue`, which is used when passing values through Pyed nodes and programs.

Pyed is meant to be a language that is truly usable in a graphical environment, which makes things awkward when Pyed programs need to be written down. Since this is early in development, we can get away with implementing a super simple text version that roughly corresponds to the ideal.

## Rough draft 0

* Each line starts with a (possibly empty) string of characters and then a colon `:`. The chars before the colon will be hashed and used as the node identifier. `ref: ...`
* Referring to a node is done with a colon and then the same string of characters. `:ref`
* One can also refer to nodes by line number, or if the id is omitted, the most-recently-defined node. `:1, :`
* Pyed builtins are indicated with a dollar sign `$` and all caps. `$STDIN, $LOOP`
* Pyed tries to infer argument -> parameter assignment from types and other info but sometimes you have to be explicit. In that case, the parameter name followed by an equals sign `=`. `cond=:in`