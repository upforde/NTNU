functor
import
    Application(exit:Exit)
    System
define
    fun {Max X Y}
        if X > Y then
            X
        else
            Y
        end
    end
    proc {PrintGreater X Y}
        {System.showInfo {Max X Y}}
    end

    {PrintGreater 10 100}
    {Exit 0}
end
