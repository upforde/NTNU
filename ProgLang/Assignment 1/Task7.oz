functor
import
    System
define
    \insert List.oz

    L = [1 2 3 4]
    L2 = [5 6]

    % Printing the lists
    {System.showInfo "The first list L: "}
    {PrintList L}
    {System.showInfo "The second list L2: "}
    {PrintList L2}

    % Testing function Length
    {System.showInfo ""}
    {System.showInfo "Length function on List L: "#{Length L}}

    % Testing function Take
    {System.showInfo ""}
    {System.showInfo "The first 2 elements taken from L: "}
    {PrintList {Take L 2}}

    % Testing function Drop
    {System.showInfo ""}
    {System.showInfo "List L with its first 2 elements dropped: "}
    {PrintList {Drop L 2}}

    % Testing function Append
    {System.showInfo ""}
    {System.showInfo "List L2 appended to list L: "}
    {PrintList {Append L L2}}

    % Testing function member
    {System.showInfo ""}
    {System.showInfo "Is 3 a member of L?"}
    if {Member L 3} then
        {System.showInfo "Yes"}
    else
        {System.showInfo "No"}
    end 
    {System.showInfo "Is 3 a member of L2?"}
    if {Member L2 3} then
        {System.showInfo "Yes"}
    else
        {System.showInfo "No"}
    end 

    % Testing function Position
    {System.showInfo ""}
    {System.showInfo "Position of number 4 in L: "#{Position L 4}}
    
end