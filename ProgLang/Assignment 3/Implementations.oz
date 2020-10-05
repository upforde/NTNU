%------------------------Task 1---------------------------

proc {QuadraticEquation A B C ?RealSol ?X1 ?X2} QEFunc Add Sub D in
    % A general function that does the quadratic equation with some operator
    % Meant to be either plus or minus, as the equation calls for +-
    fun {QEFunc A B C Op}
        {Op ~B {Float.sqrt B*B - 4.0 * A * C}} / 2.0 * A
    end

    % Function for addition
    fun {Add A B} A+B end
    % Function for subtraction
    fun {Sub A B} A-B end

    % Calculating the discriminant
    D = B*B - 4.0*A*C
    % Determening if there is real one solution
    if D == 0.0 then
        % Make RealSol true and calculate the solution
        RealSol = true
        X1 = X2 = {QEFunc A B C Add}
    % If there are multiple real solutions
    elseif D > 0.0 then 
        % Make RealSol true and calculate the solutions
        RealSol = true
        X1 = {QEFunc A B C Add}
        X2 = {QEFunc A B C Sub}
    % If there are multiple imaginary solutions
    % Set RealSol to false and don't bother calculating the solutions
    else RealSol = false end
end

% Procedure to print out the answers for the quadratic equations
% This is just to keep the code clean in Main.oz
proc {PrintQEAnswers RealSol X1 X2}
    {System.printInfo "\tThe first quadratic equation has "}
    if RealSol then 
        if X1 == X2 then {System.showInfo "a real number answer, "#X1}
        else {System.showInfo "real number answers, "#X1#" and "#X2} end
    else {System.showInfo "no real number answers"} end
end

%------------------------Task 2---------------------------

fun {Length List}
    % If the list is empty
    if List == nil then
        % stop incrementing
        0
    % If the list is not empty
    else 
        % increment and keep going down the tail
        1 + {Length List.2}
    end
end

fun {Sum List}
    % If the list is empty
    if List == nil then
        % return 0
        0
    % If the list is not empty
    else
        % Prepare the head for recursive summation with 
        % the rest of the elements in the tail
        List.1 + {Sum List.2}
    end
end

%------------------------Task 3---------------------------


fun {RightFold List Op U}
    % If the list is empty
    if List == nil then
        % return the neutral element
        U
    % If the list is not empty
    else
        % Preform the operation on the head and tail
        % of the list recursively
        {Op List.1 {RightFold List.2 Op U}}
    end
end

% Function for addition returns the sum of the parameters
fun {Add A B} A+B end

% Function for length uses a cell to keep track of how many
% times the function has been called
% Create a "global" cell
C = {NewCell 0}
fun {Len A B}
    % increment the cell value
    C:=@C+1
    % return the cell value
    @C 
end

%------------------------Task 4---------------------------

fun {Quadratic A B C} Solve in
    % Function solve takes in an X value
    fun {Solve X}
        % Returns a solution for the quadratic equation
        % using the X value provided
        A*X*X + B*X + C
    end

    % The Quadratic function returns the solve function itself
    Solve
end

%------------------------Task 5---------------------------

fun {LazyNumberGenerator StartValue} LazyNextNumber in
    % Create a function that calls the LazyNumberGenerator 
    % with an incremented value of startValue
    fun {LazyNextNumber} {LazyNumberGenerator StartValue + 1} end

    % Return a list with the start value as the first element
    % and the funtion to create a new list as the second element
    StartValue | LazyNextNumber
end

%------------------------Task 6---------------------------

fun {SumTail List Sum}
    % If the list is nil, then return the sum
    if List == nil then
        Sum
    % If not, call the function recursively and 
    % sum up the sum and the head of the list. Send
    % the tail of the list as the new list
    else
        {SumTail List.2 Sum + List.1}
    end
end

