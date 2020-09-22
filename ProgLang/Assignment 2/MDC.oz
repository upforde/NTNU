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

    fun {Tokenize Leximes}
        if Leximes == nil then
            Leximes
        elseif Leximes.1 == &+ then
            operator(type:pluss) | {Tokenize Leximes.2}
        elseif Leximes.1 == &- then
            operator(type:minus) | {Tokenize Leximes.2}
        elseif Leximes.1 == &* then
            operator(type:multiply) | {Tokenize Leximes.2}
        elseif Leximes.1 == &/ then
            operator(type:divide) | {Tokenize Leximes.2}
        else 
            number({Char.toInt Leximes.1}) | {Tokenize Leximes.2}
        end
    end
/*
    fun {Interpret Tokens}

    end
 */
    T = num(5)
    B = num(2)

    C = {IntToFloat T.1} / {IntToFloat B.1}

    {System.showInfo C}

    X = {Tokenize {Lex "1 2 + 3 *"}}
    {System.showInfo X}

end