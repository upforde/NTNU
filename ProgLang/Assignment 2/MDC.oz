functor
import
    System
define
    \insert List.oz

    % Procedure to print the list as shown in the assignment paper
    proc {PrintList List}
        % Starts by printing the open parenthesies
        {System.printInfo "("}
        % Then loops through all elements of the list
        for X in List do
            % Opens the bracket and prints the element as an atom
            {System.printInfo "["#{Char.toAtom X}}
            % Checks if it's the last element in the list
            if {Position List X} == {Length List}-1 then
                % If so, just closes the bracket
                {System.printInfo "]"}
            else
                % Otherwise adds a whitespace at the end of the bracket
                {System.printInfo "] "}
            end
        end
        % Closes the parenthesies
        {System.printInfo ")"}
        % Prints a newline
        {System.showInfo ""}
    end

    % Function for retrieving leximes from a string of whitespace-separated leximes
    fun {Lex String}
        % If the function has gone through the entire string
        if String.2 == nil then
            % Return the string
            String
        % If the current character is a space
        elseif String.1 == 32 then
            % Omit the space
            {Lex String.2}
        else 
            % If none of the above
            % keep the first character and continue down the tail
            String.1 | {Lex String.2}
        end
    end

    {PrintList {Lex "1 2 + 3 *"}}
    
end