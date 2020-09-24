functor
import
    System
define
    \insert List.oz

    % Function for retrieving leximes from a Input of whitespace-separated leximes
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
    end

    % Function for tokenizing the leximes
    fun {Tokenize Leximes}
        % If the lexime that is being checked is nil
        if Leximes == nil then
            % then the list of leximes has been parsed through and all leximes
            % have been replaced by records. Return the list
            Leximes
        % If the lexime is the "+" character
        elseif Leximes.1 == &+ then
            % then the lexime gets replaced with the operator record of type pluss
            operator(type:pluss) | {Tokenize Leximes.2}
        % If the lexime is the "-" character
        elseif Leximes.1 == &- then
            % then the lexime gets replaced with the operator record of type minus
            operator(type:minus) | {Tokenize Leximes.2}
        % If the lexime is the "*" character
        elseif Leximes.1 == &* then
            % then the lexime gets replaced with the operator record of type multiply
            operator(type:multiply) | {Tokenize Leximes.2}
        % If the lexime is the "/" character
        elseif Leximes.1 == &/ then
            % then the lexime gets replaced with the operator record of type divide
            operator(type:divide) | {Tokenize Leximes.2}
        % If the lexime is the "p" character
        elseif Leximes.1 == &p then
            % then the lexime gets replaced with the command record for print
            command(print) | {Tokenize Leximes.2}
        % If the lexime is the "d" character
        elseif Leximes.1 == &d then
            % then the lexime gets replaced with the command record for duplicate
            command(duplicate) | {Tokenize Leximes.2}
        % If the lexime is the "i" character
        elseif Leximes.1 == &i then
            % then the lexime gets replaced with the command record for invert
            command(invert) | {Tokenize Leximes.2}
        % if the lexime is the "^" character
        elseif Leximes.1 == &^ then
            % then the lexime gets replaced with the command record for inverse
            command(inverse) | {Tokenize Leximes.2}
        % If none of the above, then it's probably an int
        else 
            % the lexime gets replaced with the number record and the lexime value is turned into an int
            number({StringToInt{AtomToString{Char.toAtom Leximes.1}}}) | {Tokenize Leximes.2}
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
                    Quotient = {IntToFloat Operands.2.1.1} / {IntToFloat Operands.1.1} in
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
                        {Interpret {Append {Append {Take Stack InversePos-1} number({IntToFloat 1} / {IntToFloat {Last Stack}.1})|nil} {Drop Tokens InversePos+1}}}
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

    {System.showInfo "-------------Task 1-------------"}

    {System.showInfo "I've done the first assignment, so the List functions mentioned have allready been implemented.\n"#
    "Some new functions have been added to the List.oz file, and some old functions have been edited slightly.\n"#
    "This was done because they were specifically made as list functions. The new functions are explained with\n"# 
    "comments and such, just like the old ones are."}

    {System.showInfo "-------------Task 2-------------"}

    {System.printInfo "Task 2 a): "}
    {System.show {Lex "1 2 + 3 *"}}
    
    {System.printInfo "Task 2 b): "}
    {System.show {Tokenize {Lex "1 2 + 3 *"}}}

    {System.printInfo "Task 2 c): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 +"}}}}

    {System.printInfo "Task 2 d): The function prints; "}
    D = {Interpret {Tokenize {Lex "1 2 3 p +"}}}
    {System.printInfo "The function returns; "}
    {System.show D}

    {System.printInfo "Task 2 e): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 + d"}}}}

    {System.printInfo "Task 2 f): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 + i"}}}}

    {System.printInfo "Task 2 g): "}
    {System.show {Interpret {Tokenize {Lex "1 2 3 + ^"}}}}

    {System.showInfo ""}
    {System.showInfo "-------------Task 3-------------"}

    {System.printInfo "Task 3 b): "}
    {System.show ""}
/* 
    {System.showInfo ""}
    {System.showInfo "-------------Task 4-------------"}

    {System.printInfo "Task 4 a): "}
    {System.show ""}

    {System.printInfo "Task 4 b): "}
    {System.show ""}
    
    {System.printInfo "Task 4 c): "}
    {System.show ""}
    
    {System.printInfo "Task 4 d): "}
    {System.show ""}
*/
end