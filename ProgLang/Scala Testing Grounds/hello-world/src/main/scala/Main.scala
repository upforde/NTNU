import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent._
import scala.concurrent.duration._

object task2 {
  var lol = 10
  def main(args: Array[String]):Unit = {
    var list: List[Test] = List(new Test(), new Test(), new Test(), new Test())
    println(list)
    for (test <- list) {new Thread(test).start()}
  } 
}

class Test() extends Runnable{
  override def run() = {
    Thread.sleep(50)
    println("Fuck1")
    Thread.sleep(50)
    println("Fuck2")
  }
}