fun {Length List}
    if List == nil then
        % If the list is empty
        % stop incrementing
        0
    else 
        % If there are more things in the list
        % increment and keep going down the tail
        1 + {Length List.2}
    end
end

fun {Take List Count}
    if Count >= {Length List} then
        % Is the count equal or greater to the length of the list?
        % just return the whole list
        List
    elseif Count == 0 then
        % If the count is zero
        % just return nothing
        nil
    else 
        % If none of the above
        % keep the first entry and continue down the tail
        List.1 | {Take List.2 Count-1}
    end
end

fun {Drop List Count}
    if Count >= {Length List} then 
        % Is the count equal or greater to the length of the list?
        % just return nothing
        nil
    elseif Count == 0 then
        List
    elseif Count == 1 then
        % If only the first entry is to be dropped
        % then just return the tail
        List.2
    else
        % If none of the obove
        % continue down the List
        {Drop List.2 Count-1}
    end
end

fun {Append List1 List2}
    if List1 == nil then
        List2
    elseif List1.2 == nil then
        % Are the next entries in List1 non-existent?
        % append the first entry of List1 to the start of List2
        List1.1 | List2
    else 
        % Append the first entry of List1 to List1 tail and List2 whole List2
        List1.1 | {Append List1.2 List2}
    end
end

fun {Member List Element}
    if List.1 == Element then
        % Is the first element the one I'm looking for?
        % return true
        true
    elseif List.2 == nil then
        % if there are no more elements to check
        % then return false
        false
    else
        % Otherwise, check the tail
        {Member List.2 Element}
    end
end

fun {Position List Element}
    % Check to see if the element is even in the list
    if {Member List Element} then
        % If it is, then the search for the element begins
        if List.1 == Element then
            % If the element I'm looking at is the one I'm looking for
            % then stop incrementing
            0
        else 
            % If not, then increment and check the tail
            1 + {Position List.2 Element}
        end
    else 
        % If the element is not a member of the list, then some value is
        % returned to indicate this. I chose the length of the list, because
        % this function returns positions starting from zero, meaning that
        % the polsition of the last element in the list will be one less 
        % than the length of the list.
        {Length List}
    end
end

fun {Last List}
    % If the list is empty, then return nil
    if List == nil then
        nil
    % If the tail is empty, then return the first element, as 
    % it is the last element
    elseif List.2 == nil then
        List.1
    % If not, call the function recursively, and give the tail 
    % as the new list.
    else 
        {Last List.2}
    end
end