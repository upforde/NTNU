functor
import
    System
define
    proc {Circle R}
        local 
            Pi = {Float.'/' 355.0 113.0}
            A = Pi * R * R
            D = 2.0*R
            C = Pi*D
        in
            {System.showInfo "Area: "#A#", Diameter: "#D#", Circumference: "#C}
        end
    end

    {Circle 1.0}
end
