functor
import
    System
define
    \insert List.oz

    % This function is commented out, because it could only handle intigers from 0-9
    % but not 10 and not floats. I therefore switched to the String.tokens function below.
    % The rest of the code had to be slightly modified aswell to work with the new
    % String method instead of my own function.

    /* % Function for retrieving leximes from a Input of whitespace-separated leximes
    fun {Lex Input}
        % If the function has gone through the entire Input
        if Input.2 == nil then
            % Return the Input
            Input
        % If the current character is a space
        elseif Input.1 == &  then
            % Omit the space
            {Lex Input.2}
        else 
            % If none of the above
            % keep the first character and continue down the tail
            Input.1 | {Lex Input.2}
        end
    end*/

    % Function for retrieving leximes from a Input of whitespace-separated leximes
    fun {Lex Input}
        % Uses the String.tokens method to retrieve a set of strings, where each
        % member is the string inbetween the whitespaces in the original Input string
        {String.tokens Input & }
    end

    % Function for tokenizing the leximes
    fun {Tokenize Leximes}
        % If the lexime that is being checked is nil
        if Leximes == nil then
            % then the list of leximes has been parsed through and all leximes
            % have been replaced by records. Return the list
            Leximes
        % If the lexime is the "+" character
        elseif Leximes.1.1 == &+ then
            % then the lexime gets replaced with the operator record of type pluss
            operator(type:pluss) | {Tokenize Leximes.2}
        % If the lexime is the "-" character
        elseif Leximes.1.1 == &- then
            % then the lexime gets replaced with the operator record of type minus
            operator(type:minus) | {Tokenize Leximes.2}
        % If the lexime is the "*" character
        elseif Leximes.1.1 == &* then
            % then the lexime gets replaced with the operator record of type multiply
            operator(type:multiply) | {Tokenize Leximes.2}
        % If the lexime is the "/" character
        elseif Leximes.1.1 == &/ then
            % then the lexime gets replaced with the operator record of type divide
            operator(type:divide) | {Tokenize Leximes.2}
        % If the lexime is the "p" character
        elseif Leximes.1.1 == &p then
            % then the lexime gets replaced with the command record for print
            command(print) | {Tokenize Leximes.2}
        % If the lexime is the "d" character
        elseif Leximes.1.1 == &d then
            % then the lexime gets replaced with the command record for duplicate
            command(duplicate) | {Tokenize Leximes.2}
        % If the lexime is the "i" character
        elseif Leximes.1.1 == &i then
            % then the lexime gets replaced with the command record for invert
            command(invert) | {Tokenize Leximes.2}
        % if the lexime is the "^" character
        elseif Leximes.1.1 == &^ then
            % then the lexime gets replaced with the command record for inverse
            command(inverse) | {Tokenize Leximes.2}
        % If none of the above, then it's probably an int
        else 
            % the lexime gets replaced with the number record and the lexime value is turned into an int
            number({StringToFloat Leximes.1}) | {Tokenize Leximes.2}
        end
    end

    % Function that interprets the tokens and does the calculations
    fun {Interpret Tokens}
        % Local variables used in the function 
        % These variables house the position of each operator or command that is in the tokens
        local PlusPos = {Position Tokens operator(type:pluss)}
        MinusPos = {Position Tokens operator(type:minus)}
        MultiPos = {Position Tokens operator(type:multiply)}
        DivPos = {Position Tokens operator(type:divide)} 
        PrintPos = {Position Tokens command(print)}
        DupePos = {Position Tokens command(duplicate)}
        InvertPos = {Position Tokens command(invert)}
        InversePos = {Position Tokens command(inverse)}
        % The last two variables are Length, which holds the Token length so that
        % the function doesn't need to run as many times, and Smallest, which is 
        % a variable reserved for a function
        Len = {Length Tokens} Smallest in

            % The function smallest checks which position closest to the left and returns the position
            fun {Smallest}
                local All = [PlusPos MinusPos MultiPos DivPos PrintPos DupePos InvertPos InversePos] in
                    {List.sort All Value.'<'}.1
                end
            end
            
            % This code checks if there are any operators or commands left in Tokens. If a position is the same as the 
            % length of Tokens, then it means that there aren't any more operators or commands of that type in Tokens
            if {And 
                    {And
                        {And PlusPos == Len MinusPos == Len}
                        {And MultiPos == Len DivPos == Len}
                    }
                    {And
                        {And PrintPos == Len DupePos ==  Len}
                        {And InvertPos == Len InversePos == Len}
                    }
                } then
                Tokens
            else
                % If the closest operator or command to the left is the pluss operator
                if {Smallest} == PlusPos then
                    % Make local variables that get the two predescessors to the operator and sum them together
                    local Operands = {Drop {Take Tokens PlusPos} PlusPos-2}
                    Sum = Operands.1.1 + Operands.2.1.1 in
                        % After summing the values, the two predescessors to the operator together with the operator
                        % get replaced by the new record of the sum, and the function gets recursively called to 
                        % check for other operators or commands
                        {Interpret {Append {Append {Take Tokens PlusPos-2} number(Sum) | nil} {Drop Tokens PlusPos+1}}}
                    end
                % If the closest operator or command to the left is the minus operator
                elseif {Smallest} == MinusPos then
                    % Make local variables that get the two predescessors to the operator and calculate their difference
                    local Operands = {Drop {Take Tokens MinusPos} MinusPos-2}
                    Difference = Operands.2.1.1 - Operands.1.1 in
                        % After calculating the difference, the two predescessors to the operator together with the operator
                        % get replaced by the new record of the difference, and the function gets recursively called to 
                        % check for other operators or commands
                        {Interpret {Append {Append {Take Tokens MinusPos-2} number(Difference) | nil} {Drop Tokens MinusPos+1}}}
                    end
                % If the closest operator or command to the left is the multiply operator
                elseif {Smallest} == MultiPos then
                    % Make local variables that get the two predescessors to the operator and multiply them together
                    local Operands = {Drop {Take Tokens MultiPos} MultiPos-2}
                    Product = Operands.1.1 * Operands.2.1.1 in
                        % After multiplying the values, the two predescessors to the operator together with the operator
                        % get replaced by the new record of the product, and the function gets recursively called to 
                        % check for other operators or commands
                        {Interpret {Append {Append {Take Tokens MultiPos-2} number(Product) | nil} {Drop Tokens MultiPos+1}}}
                    end
                % If the closest operator or command to the left is the devide operator
                elseif {Smallest} == DivPos then
                    % Make local variables that get the two predescessors to the operator and divide them by one another
                    local Operands = {Drop {Take Tokens DivPos} DivPos-2}
                    Quotient = Operands.2.1.1 / Operands.1.1 in
                        % After dividing the values, the two predescessors to the operator together with the operator
                        % get replaced by the new record of the quotient, and the function gets recursively called to 
                        % check for other operators or commands
                        {Interpret {Append {Append {Take Tokens DivPos-2} number(Quotient) | nil} {Drop Tokens DivPos+1}}}
                    end
                % If the closest operator or command to the left is the print command
                elseif {Smallest} == PrintPos then
                    % Make a local variable that holds the Stack
                    local Stack = {Take Tokens PrintPos} in
                        % The stack gets printed
                        {System.show Stack}
                        % The print command is removed and the function gets called recursively to theck for other operators or commands
                        {Interpret {Append Stack {Drop Tokens PrintPos+1}}}
                    end
                % If the closest operator or command to the left is the duplicate command
                elseif {Smallest} == DupePos then
                    % Make a local variable that holds the Stack
                    local Stack = {Take Tokens DupePos} in
                        % The duplicate command is replaced by a dublicate of the top element in the stack
                        % and the function gets called recursively to theck for other operators or commands
                        {Interpret {Append {Append Stack {Last Stack} | nil} {Drop Tokens DupePos+1}}}
                    end
                elseif {Smallest} == InvertPos then
                    % Make a local variable that holds the Stack
                    local Stack = {Take Tokens InvertPos} in
                        % The Invert command, together with the top element in the stack, is replaced by a
                        % negative version of the top element in the stack and the function gets called
                        % recursively to check for other operators or commands
                        {Interpret {Append {Append {Take Stack InvertPos-1} number(~{Last Stack}.1)|nil} {Drop Tokens InvertPos+1}}}
                    end
                elseif {Smallest} == InversePos then
                    % Make a local variable that holds the Stack
                    local Stack = {Take Tokens InversePos} in
                        % The Inverse command, together with the top element in the stack, is replaced by the
                        % inverse of the top element in the stack and the function gets called recursively to 
                        % check for other operators or commands
                        {Interpret {Append {Append {Take Stack InversePos-1} number({IntToFloat 1} / {Last Stack}.1)|nil} {Drop Tokens InversePos+1}}}
                    end
                % This else Tokens is here because I want to show which operator or command each if or elseif belongs to
                else 
                    Tokens
                end
            % Two positions will never be equal because only one operator or command can occupy one position at a time, which is why checking 
            % which operator or command is the closest by the position it occupies in Tokens works.
            end
        end
    end

    % Function that translates the expression from Reverse-Polish-Notation to Infix notation.
    fun {InfixInternal Tokens ExpressionStack}
        % Checks if all tokens have been checked
        if Tokens == nil then
            % Returns the expression stack
            ExpressionStack
        % If not all tokens have been checked
        else
            % If the token is a number
            case Tokens.1 of number(N) then
                % Appends the token to the expression stack and calls the function recursively
                % with the tail of the tokens as Tokens and the new expression stack as ExpressionStack
                {InfixInternal Tokens.2 {Append ExpressionStack number(N)|nil}}
            % If the token is the pluss operator
            [] operator(type:pluss) then
                % Create a local variable which houses the top two entries in the ExpressionStack
                local NewExpressionStack = {Drop ExpressionStack {Length ExpressionStack}-2} 
                % Concatinates the top two entries in the Expression stack into a new entrie that
                % is in the Infix notation
                NewString = "( "#NewExpressionStack.2.1.1#" + "#NewExpressionStack.1.1#" ) " in
                    % Removes the top two entries from the ExpressionStack and appends the new Infix notation as a new
                    % record called 'infix(string)'. The record is there to avoid any problems in the recursive hadling 
                    % of the data, since all other entries in the stack are records of type (most likely) numbers 
                    {InfixInternal Tokens.2 {Append {Take ExpressionStack {Length ExpressionStack}-2} infix(NewString)|nil}}
                end
            [] operator(type:minus) then
                % Create a local variable which houses the top two entries in the ExpressionStack
                local NewExpressionStack = {Drop ExpressionStack {Length ExpressionStack}-2} 
                % Concatinates the top two entries in the Expression stack into a new entrie that
                % is in the Infix notation
                NewString = "( "#NewExpressionStack.2.1.1#" - "#NewExpressionStack.1.1#" ) " in
                    % Removes the top two entries from the ExpressionStack and appends the new Infix notation as a new
                    % record called 'infix(string)'. The record is there to avoid any problems in the recursive hadling 
                    % of the data, since all other entries in the stack are records of type (most likely) numbers 
                    {InfixInternal Tokens.2 {Append {Take ExpressionStack {Length ExpressionStack}-2} infix(NewString)|nil}}
                end
            [] operator(type:multiply) then
                % Create a local variable which houses the top two entries in the ExpressionStack
                local NewExpressionStack = {Drop ExpressionStack {Length ExpressionStack}-2} 
                % Concatinates the top two entries in the Expression stack into a new entrie that
                % is in the Infix notation
                NewString = "( "#NewExpressionStack.2.1.1#" * "#NewExpressionStack.1.1#" ) " in
                    % Removes the top two entries from the ExpressionStack and appends the new Infix notation as a new
                    % record called 'infix(string)'. The record is there to avoid any problems in the recursive hadling 
                    % of the data, since all other entries in the stack are records of type (most likely) numbers 
                    {InfixInternal Tokens.2 {Append {Take ExpressionStack {Length ExpressionStack}-2} infix(NewString)|nil}}
                end
            [] operator(type:divide) then
                % Create a local variable which houses the top two entries in the ExpressionStack
                local NewExpressionStack = {Drop ExpressionStack {Length ExpressionStack}-2} 
                % Concatinates the top two entries in the Expression stack into a new entrie that
                % is in the Infix notation
                NewString = "( "#NewExpressionStack.2.1.1#" / "#NewExpressionStack.1.1#" ) " in
                    % Removes the top two entries from the ExpressionStack and appends the new Infix notation as a new
                    % record called 'infix(string)'. The record is there to avoid any problems in the recursive hadling 
                    % of the data, since all other entries in the stack are records of type (most likely) numbers 
                    {InfixInternal Tokens.2 {Append {Take ExpressionStack {Length ExpressionStack}-2} infix(NewString)|nil}}
                end
            % If the token did not match any cases above, then it's either a command, or some other invalid token
            % and just gets disregarded. The function is called recursively with the tail of Tokens as Tokens and the
            % current ExpressionStack as ExpressionStack
            else
                {InfixInternal Tokens.2 ExpressionStack}
            end
        end
    end

    % Function that calls the InfixInternal function
    fun {Infix Tokens}
        % The function returns only the virtual string that gets generated by the InfixInternal function
        % The InfixInternal function actually returns a list of entries in the expression stack. If the 
        % Reverse-Polish-Notation leximes were of a valid format, then the first entry in the stack will
        % be a record of type infix(string) with its value being the string which is the translated Infix
        % notation of the leximes. Some error handling can be implemented here, but the task didn't ask for
        % any, which is why none has been implemented.
        {InfixInternal Tokens nil}.1.1
    end
    

    {System.showInfo "-------------Task 1-------------"}

    {System.showInfo "I've done the first assignment, so the List functions mentioned have allready been implemented.\n"#
    "Some new functions have been added to the List.oz file, and some old functions have been edited \n"#
    "slightly. This was done because they were specifically made as list functions. The new functions\n"# 
    "are explained with comments and such, just like the old ones are."}

    {System.showInfo "-------------Task 2-------------"}

    {System.printInfo "Task 2 a): "}
    {System.show {Lex "1 2 + 3 *"}}
    
    {System.showInfo " "}
    {System.printInfo "Task 2 b): "}
    {System.show {Tokenize {Lex "1 2 + 3 *"}}}

    {System.showInfo " "}
    {System.printInfo "Task 2 c): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 +"}}}}

    {System.showInfo " "}
    {System.printInfo "Task 2 d): The function prints; "}
    D = {Interpret {Tokenize {Lex "1 2 3 p +"}}}
    {System.printInfo "The function returns; "}
    {System.show D}

    {System.showInfo " "}
    {System.printInfo "Task 2 e): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 + d"}}}}

    {System.showInfo " "}
    {System.printInfo "Task 2 f): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 + i"}}}}

    {System.showInfo " "}
    {System.printInfo "Task 2 g): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 + ^"}}}}

    {System.showInfo ""}
    {System.showInfo "-------------Task 3-------------"}

    {System.printInfo "Task 3 b): "}
    {System.showInfo {Infix {Tokenize {Lex "3.0 9.0 10.0 * - 0.3 +"}}}}

    {System.showInfo ""}
    {System.showInfo "-------------Task 4-------------"}

    {System.showInfo "Task 4 a):"}
    {System.showInfo "<operator> ::= + | - | * | /\n"#
    "<command>  ::= p | d | i | ^\n"#
    "<number>   ::= [0...9]*\n             | [0...9]*.[0...9]*"}

    {System.showInfo " "}
    {System.showInfo "Task 4 b):"}
    {System.showInfo "<expression> ::= (<number><operator><number>)\n"#
    "               | (<expression><operator><number>)\n"#
    "               | (<number><operator><expression>)\n"#
    "               | (<expression><operator><expression>)"}
    {System.showInfo "The way I set up this grammar is inambiguous, because the operator and operands are being wrapped\n"#
    "inside of parenthesies, making the precedence of each operator obsolete. I don't allow for <number> to be a valid\n"#
    "expression, as this can make '1' a valid expression, which I don't want."}
    
    {System.showInfo " "}
    {System.printInfo "Task 4 c): "}
    {System.showInfo "A context-free grammar is a grammar with rules that allow for any non-terminal symbol to produce\n"#
    "strings of terminal and/or non-terminal symbols.\n"#
    "V --> w where 'V' is any non-terminal symbol in the grammar alphabet and 'w' is some string of terminal and/or\n"#
    "non-terminal symbols.\n\n"#
    "A context-sensitive grammar is a grammar with rules that allow for a non-terminal symbol to produce some string\n"#
    "of terminal and/or non-terminal symbols only if some specific terminal and/or non-terminal symbol or a specific\n"#
    "string of terminal and/or non-terminal symbols is present. In other words, a non-terminal symbol has to be surounded\n"#
    "by some context of terminal and/or non-terminal symbols in order to produse some string of terminal and/or non-terminal\n"#
    "symbols.\n"#
    "xV --> w where 'V' is any non-terminal symbol in the grammar alphabet, 'w' is some string of terminal and/or\n"#
    "non-terminal symbols and 'x' is some string of terminal and/or non-terminal symbols that has to be present so\n"#
    "that the production rule can be enacted."}
    
    {System.showInfo " "}
    {System.printInfo "Task 4 d): "}
    {System.showInfo "This happens because values of type integer and values of type float have different operations associated\n"#
    "with them. One simple example is division of integers vs division of floats. When integers are divided, the answer is rounded\n"#
    "down (3/2=1) while when floats are divided, the answer is stored with some number of decimals (3.0/2.0=1.5). While I haven't \n"#
    "done anything like this in the tasks, this error can be used for pattern matching purposes. An example of this in this task could\n"#
    "be finding out which operator is being used by trying to execute an operation with an operator and catching the error. If there was\n"#
    "a type mismatch, then we know that a division has occured, and we can handle that accordingly."}

end