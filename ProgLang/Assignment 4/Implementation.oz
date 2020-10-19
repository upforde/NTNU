fun {GenerateOdd S E}
    if {Int.isOdd S} andthen S =< E then
        S | {GenerateOdd S+2 E}
    elseif {Int.isEven S} andthen S+1 =< E then
        S+1 | {GenerateOdd S+3 E} 
    else nil end
end

fun {Product S}
    if S == nil then 1
    else
        S.1 * {Product S.2}
    end
end

/*
fun lazy {LazyGenerateOdd S E}
    if {Int.isOdd S} andthen S =< E then
        S | {GenerateOdd S+2 E}
    elseif {Int.isEven S} andthen S+1 =< E then
        S+1 | {GenerateOdd S+3 E} 
    else nil end
end
*/