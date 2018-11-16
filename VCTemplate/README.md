# Template Language

## Placeholder
The placeholder is a Python expression that is evaluated to a string and inserted
into the resulting document where it was placed.

The placeholder has the following syntax:

```
${<Python expression>}
```

The placeholder can also be used to escape the `$` and `%` characters, for example:

```
${"$"} or ${"%"}
```

## Python code
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

## Including
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

## If statement

## For loop

## While loop

## Do-while loop

## Function


