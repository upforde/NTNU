functor 
import 
    Application
    System
define
    \insert Implementations.oz

%------------------------Task 1---------------------------
    {System.showInfo "Task 1:"}
    {System.printInfo "a)"}
    local RealSol1 RealSol2 X11 X12 X21 X22 in
        {QuadraticEquation 2.0 1.0 ~1.0 RealSol1 X11 X21}
        {PrintQEAnswers RealSol1 X11 X21}

        {QuadraticEquation 2.0 1.0 2.0 RealSol2 X12 X22}
        {PrintQEAnswers RealSol2 X12 X22}
    end
    
    {System.showInfo "b)\tProcedural abstraction encloses a statement, giving it a contextual"#
    "\n\tenvironment that ensures that the statement executes the same way"#
    "\n\tevery time it is called. It allso allows for the same statement to"#
    "\n\tbe called in multiple places."}
    {System.showInfo "c)\tA function has some sort of return value (be it a value of an integer,"#
    "\n\ta tuple, a record, a function etc.) while a procedure does not."}

%------------------------Task 2---------------------------

    {System.showInfo "\nTask 2:"}
    {System.showInfo "\tThe sum of elements in list [1 2 3 4 5] is "#{Sum [1 2 3 4 5]}}
    {System.showInfo "\tThe length of list [1 2 3 4 5] is "#{Length [1 2 3 4 5]}}

%------------------------Task 3---------------------------

    {System.showInfo "\nTask 3:"}
    {System.showInfo "c)\tThe sum of elements in list [1 2 3 4 5] is "#{RightFold [1 2 3 4 5] Add 0}}
    {System.showInfo "\tThe length of list [1 2 3 4 5] is "#{RightFold [1 2 3 4 5] Len 0}}
    {System.showInfo "d)\tLeft fold would not affect the Sum and Length operations because"#
    "\n\tthese operations are commutative, meaning they are independent of"#
    "\n\torder of operations. Subtraction, however, is noncommutative, meaning"#
    "\n\tthat the order of operations does matter, which in turn means that"#
    "\n\tcalculations would be affected."}
    {System.showInfo "e)\tA good value for U when implementing multiplication is 1, because"#
    "\n\tmultiplication by 1 does not change the initial value."}

%------------------------Task 4---------------------------

    {System.showInfo "Task 4:"}
    {System.showInfo "\tf(X) equals to "#{{Quadratic 3 2 1} 2}}

%------------------------Task 5---------------------------

    {System.showInfo "Task 5:"}
    {System.showInfo "a)\tNumber generated by the LazyNumberGenerator:"#{{{{{{LazyNumberGenerator 0}.2}.2}.2}.2}.2}.1}
    {System.showInfo "b)\tSince the function returns a list consisting of the original value and a"#
    "\n\tfunction callable to call the LazyNumberGenerator with an incremented"#
    "\n\tvalue, the incremented value will not be generated until the callable"#
    "\n\tis executed, i.e. by surrounding it with curly bracets. The drawback "#
    "\n\tof this method would be the extremely cumbersome way to use it."}

%------------------------Task 6---------------------------
    
    {System.showInfo "Task 6:"}
    {System.showInfo "a)\tMy sum function is not tail recursive. A tail recursive function is a"#
    "\n\tfunction that sends its current state along with the parameters when "#
    "\n\tit's called, making it the last thing that the function does."}
    {System.showInfo "\tMy implementation of the tail recursive sum function outputs "#{SumTail [1 2 3 4 5] 0}}
    {System.showInfo "b)\tBy implementing tail recursion, the function doesn't have to collapse on"#
    "\n\titself to calculate the return value. Oz is designed to use this advantage"#
    "\n\tfor optimization purposes."}
    {System.showInfo "c)\tNot all languages would benefit from tail recursion, as not all languages"#
    "\n\tprovide optimization for it. Since Oz does, then the preformance gain is"#
    "\n\tnoteworthy, but other strict functional languages evaluate all their "#
    "\n\targument first before executing the function, meaning there is no"#
    "\n\tpreformance gain"}

    {Application.exit 0}
end