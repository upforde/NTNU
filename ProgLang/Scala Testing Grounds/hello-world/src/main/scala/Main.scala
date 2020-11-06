import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent._
import scala.concurrent.duration._

object task2 {
  var lol = 10
  def main(args: Array[String]):Unit = {
    
    var answer = test(-10)
    println(answer)
    println(lol)
  }
  def test(t: Int): Either[Unit, String] = this.synchronized{
    if (t < 0 || t > 10)
      return Right("What the fuck")
    Left(lol+=t)
  }
}