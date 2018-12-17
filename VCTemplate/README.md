# Template Language

This template language was designed for code generation for different languages
but specifically for VHDL. The language was inspired by makotemplate.org, but with
a simpler data model making it more easy to do more complicated stuff.

## Data model
Like Python all assignments at the top level of a file will be added to the
shared locals/globals dictionary. Inside functions all assignments are done
in the locals dictionary.

Unlike the Python import statement, the %include statement includes the file inline
with the text that has the %include statement and any assignments done in an include
file are added to the shared locals/globals dictionary.

## Syntax

### Placeholder
The placeholder is a Python expression that is evaluated to a string and inserted
into the resulting document where it was placed.

The placeholder has the following syntax:

```
%{<Python expression>}
```

The placeholder can also be used to escape the `%` character, for example:

```
%{"%"}
```

### Python code
You can execute a Python code directly in the template, this is mostly useful for importing
external Python code or to calculate something that will be formated later by the template.

Python code is prefixed with `%%` characters, continues lines are executed as a single Python
suite. The indentation of the first line is removed from all lines in the suite. Here is the syntax:

```
%% <Python line 1>
%% <Python line 2>
%% <Python line ...>
%% <Python line n>
```

The following is an example on how to import Python code:

```
%% import os.path
${os.path.join("/foo", "bar")}
```

### Including
You can include another template in your current template.
The execution of included template is done at the place where the `%include` statement is inserted
in the text.

The `%include` statement can only appear at the top-level of each file, i.e. it can not be included 
in the body of a flow-control statement.

The `%include` statement is evaluated during parsing, included files are parsed before rendering takes
place.

Functions that are included by the `%include` statements are available in the globals namespace by the
file that is including another a file, and by other files that are being included.

When the `<filename>` argument is relative, the file is located relative to the current file.

There is no protection against including a file multiple times or recursivly.

Syntax:
```
%include <filename>
```

### If statement
Conditional `%if` statement, with optional `%elif` statments and optional end `%else` statement.
The expression in the `%elif` statements are only executed if the result of the previous `%if` or `%else`
was `False`.

```
%if <Python expression 1>
<block 1>
%elif <Python expression 2>
<block 2>
%elif <Python expression ...>
<block ...>
%else
<block n>
%end
```

### For loop
A for loop iterates over the result in the Python expression. Each iteration-result is
assigned to the name in front of the `in` keyword, optionally the iteration-result is
unpacked into multiple names.

The `%else` part of the for loop is only executed when the result of the Python expression
had zero items.

A local `loop` variable is available inside the block. It has the attributes `first`, `last` and `i`
for often used information to format code properly. The `outer` attribute is used to get information
for the next output loop.

```
%for <name(s)> in <Python expression>
<block>
%else
<block>
%end
```

### While loop
A while loop executes a block multiple times until the Python expression returns `False`.

A local `loop` variable is available inside the block. It has the attributes `first` and `i`
for often used information to format code properly. The `outer` attribute is used to get information
for the next outer loop.

```
%while <Python expression>
<block>
%end
```

### Do-while loop
A do-while loop executes a block at least once until the Python expression returns `False`.

A local `loop` variable is available inside the block. It has the attributes `first` and `i`
for often used information to format code properly. The `outer` attribute is used to get information
for the next outer loop.

```
%do
<block>
%while <Python expression>
```

### Continue
Stop executing of a block inside a loop, then continue with the next iteration of the loop.

```
%continue
```

### Break
Stop executing of a block inside a loop, then break out of the loop.

```
%break
```

### Function
Define a function that can be called in expressions.
A function with a return statement will simply return with its value.
A function without a return statement will return its textual-output.

Functions with the same name will replace the previously defined function.
The previously defined function is available as `prior()` inside the block.
This functionaliy together with the `%include` statement can be used for
as a simple form of object-oriented-polymorphism.

```
%function <name>(<arguments>)
<block>
%end
```

```
%function <name>(<arguments>)
<block>
${prior()}
<block>
%end
```

### Return
Return a Python object from a function.

```
%return <Python expression>
```

### Named block
This simply executes the block where it was defined. When a block of the same
name is defined later it instead is executed in place of the first. A block
of the same name will only be implicently executed once, in place of the first
definition.

A block is a function without arguments, which is directly called after its
definition.

The previously defined block is available as `prior()` inside the block.
This functionaliy together with the `%include` statement can be used for
as a simple form of object-oriented-polymorphism.

```
%block <name>
<block>
%end
```

