functor 
import 
    Application
    System
define
    \insert Implementations.oz

%------------------------Task 1---------------------------
    {System.showInfo "Task 1:"}
    {System.printInfo "a)"}
    RealSol1 RealSol2 X11 X12 X21 X22

    {QuadraticEquation 2.0 1.0 ~1.0 RealSol1 X11 X21}
    {PrintQEAnswers RealSol1 X11 X21}

    {QuadraticEquation 2.0 1.0 2.0 RealSol2 X12 X22}
    {PrintQEAnswers RealSol2 X12 X22}
    
    {System.showInfo "b)\t"}
    {System.showInfo "c)\t"}

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

{System.show {{Quadratic 3.0 2.0 1.0} 2}}

%------------------------Task 5---------------------------

%------------------------Task 6---------------------------
 
    {Application.exit 0}
end