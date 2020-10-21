% Function for generating odd numbers between S and E
fun {GenerateOdd S E}
    % If a number is odd and also less than or equal to E
    if {Int.isOdd S} andthen S =< E then
        % Return a list of S as the head and the
        % recursive call of the function with S+2 
        % as the tail
        S | {GenerateOdd S+2 E}
    % If the number is even and is less than or equal to E when incremented
    elseif {Int.isEven S} andthen S+1 =< E then
        % Return a list of S+1 as the head and the
        % recursive call of the function with S+3 
        % as the tail
        S+1 | {GenerateOdd S+3 E} 
    % If the number is bigger than E, then return nil
    else nil end
end


% Function for multiplying every number in a list together
fun {Product S}
    % If S has a head and tail
    case S of H|T then
        % return the product of the head with the 
        % value of the Product function called recursively
        H * {Product T}
    % If the list is nil
    [] nil then
        % return the identity multiplicator
        1
    end
end


% Function that lazily generates odd numbers from S to E 
% Will not comment this code, as it is identical to the 
% function GenerateOdd.
fun lazy {LazyGenerateOdd S E}
    if {Int.isOdd S} andthen S =< E then
        S | {GenerateOdd S+2 E}
    elseif {Int.isEven S} andthen S+1 =< E then
        S+1 | {GenerateOdd S+3 E} 
    else nil end
end


% The random int function taken straight out of the assignment
% Since it's not my code, I won't comment it
fun {RandomInt Min Max}
    X = {OS.rand} MinOS MaxOS in
    {OS.randLimits ?MinOS ?MaxOS}
    Min + X*(Max - Min) div (MaxOS - MinOS)
end


% The lazy HammerFactory function returns a list of hammers
% that are working 90 percent of the time
fun lazy {HammerFactory} Rnd = {RandomInt 0 100} in
    % Wait a second
    {Time.delay 1000}
    % Roll a d100 die, and if it's less than 10
    if Rnd < 10 then
        % return a defect hammer, and call the function 
        % recursively
        defect | {HammerFactory}
    % Otherwise
    else
        % return a working hammer, and call the function
        % recursively
        working | {HammerFactory}
    end
end


% The HammerConsumer function that returns the amount of working hammers in the stream
fun {HammerConsumer HammerStream N} WorkingHammerCounter in
    % Define a function for actually looking up and counting the N first 
    % elements in the stream, and also counting the hammers that are working
    fun {WorkingHammerCounter StreamedHams Counter Working}
        % Check if the counter has reached zero
        if Counter > 0 then
            % if not, then check if the first element is working
            if StreamedHams.1 == working then
                % Call the function recursively, decrementing the counter and
                % incrementing working
                {WorkingHammerCounter StreamedHams.2 Counter-1 Working+1}
            % if the first element is not working
            else
                % Call the function recursively, decrementing the counter but not 
                % incrementing working
                {WorkingHammerCounter StreamedHams.2 Counter-1 Working}
            end
        % If the counter has reached zero
        else
            % Return the amount of working elements
            Working
        end
    end

    % The counter function gets called, and when finished, returns the number of
    % working hammers in the stream, making this function return the same number
    {WorkingHammerCounter HammerStream N 0}
end


% The function that returns a buffer of size N
% The code is taken from page 291 in CTMCP
fun {BoundedBuffer In N}
    % The end variable is a list of future variables
    % not generated yet by the lazy function
    End = thread {List.drop In N} end
    % The lazy loop returns a list of elements of size N,
    % but can get more elements out of the stream if needed
    fun lazy {Loop In End}
        % checking if the In list is not empty
        case In of I|In2 then
            % returning a list of the head element and 
            % and the value of the recursive function call
            I|{Loop In2 thread End.2 end}
        end
    end
    in 
    % The Loop function is called, returning a buffer
    {Loop In End}
end
