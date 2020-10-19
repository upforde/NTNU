functor
import
    System
    Application
define
    \insert Implementation.oz

    {System.show {GenerateOdd ~3 10}}
    {System.show {GenerateOdd 3 3}}
    {System.show {GenerateOdd 2 2}}

    {System.show {Product [1 2 3 4]}}

    local Streamed Hams in
        thread Streamed = {GenerateOdd 0 1000} end
        thread Hams = {Product Streamed} end
        {System.showInfo Hams}
    end
    
    /*
    local Streamed Hams in
        thread Streamed = {LazyGenerateOdd 0 1000} end
        thread Hams = {Product Streamed} end
        {System.showInfo Hams}
    end
    */

    {Application.exit 0}
end