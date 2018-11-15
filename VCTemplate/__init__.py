"""Parse a text file as a template.

Placeholders:
    ${ <expr> }

Python execution:
    ## <python line>
    ## <python line>
    ## <python line>

Statements:
    #if <expr>
    #elif <expr>
    #else
    #end

    #for <name(s)> in <expr>
    #break
    #continue
    #end

    #while <expr>
    #end

    #function <name>(<argument(s)>)
    #return <expr>
    #end

    #method <name>
    #end

    #include <filename>
    #inherint <filename>
"""

