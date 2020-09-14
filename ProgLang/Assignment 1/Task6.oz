functor
import
    System
define
    fun {Factorial N}
        if N > 0 then
            N * {Factorial N-1}
        else
            1
        end
    end
    {System.showInfo {Factorial 3}}
    {System.showInfo {Factorial 4}}
    {System.showInfo {Factorial 5}}
    {System.showInfo {Factorial 0}}
end
