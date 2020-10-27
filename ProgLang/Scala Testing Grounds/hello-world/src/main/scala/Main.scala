object Main {
  def main(args: Array[String]):Unit = {
    // a) Generating the array. (1 to 50) is the
    // same as doing a for loop from i = 1 until i == 50
    val array = (1 to 50).toArray 

    println(sum(array))
    println(recSum(array))
    println(nthFib(10000))
  }

  // b) fucntion that sums an array using a for loop
  def sum(a:Array[Int]) = {
    var sum = 0
    for (i<-a) sum += i
    sum
  }

  // c) Function that sums an array recursively
  def recSum(a:Array[Int]):Int = a match {    //Similarly to oz, the scala programing
    case Array() => 0                         //language implements pattern matching
    case ht => ht.head + recSum(ht.tail)      //making this quite easy to implement
  }

  // d) Function that returns the nth number of the Fibonacci sequence.
  def nthFib(n: BigInt): BigInt = {
    val Zero = BigInt(0)                                                
    def fib_tail(n: BigInt, a: BigInt, b: BigInt): BigInt = n match {
      case Zero => a
      case _ => fib_tail(n - 1, b, a + b)
    }
    return fib_tail(n, 0 , 1)
  }
}