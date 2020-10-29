import scala.concurrent.ExecutionContext.Implicits.global
import scala.concurrent._
import scala.concurrent.duration._

object task2 {
  private var counter: Int = 0
  
  def main(args: Array[String]):Unit = {
    val counterThread1 = thread {increaseCounter()}
    val counterThread2 = thread {increaseCounter()}
    val printerThread = thread {printCounter()}
    val syncCounter1 = thread {syncIncreaseCounter()}
    val syncCounter2 = thread {syncIncreaseCounter()}
    val newPrinterThread = thread {printCounter()}

    // running the non-thread-safe counter function
    counterThread1.start()
    counterThread2.start()
    printerThread.start()

    // resetting the counter
    counterThread2.join(); printerThread.join()
    counter = 0

    // running the thread-safe counter function
    syncCounter1.start()
    syncCounter2.start()
    // the join here is to ensure that the printer 
    // thread runs after the two counter threads are 
    // finished.
    syncCounter2.join()
    newPrinterThread.start()

    Deadlock.run
  }

  // a) Function that takes in a body of code and returns a thread
  def thread(body: => Unit): Thread = {
    val t = new Thread { override def run() = body }
    t
  }

  def increaseCounter(): Unit = {counter += 1}
  // b) Function that prints the current counter variable
  def printCounter(): Unit = {println(s"Current counter: $counter")}

  // b) The print output is not consistent, sometimes the counter is 1
  // and sometimes it's 2. This phenominon is called nondeterminism.
  // Nondeterminism might become problematic if atomicity is absolutely
  // needed in the application. An example of this might be a bank 
  // transaction where a person recieves money from two different people.
  // If the transactions are not atomic, then one of the transactions might
  // override the other, resulting in money from the first transaction to 
  // be lost.
  
  // c) Function that increases the counter atomically
  def syncIncreaseCounter(): Unit = this.synchronized {counter += 1}

  // d) A deadlock occurs when two (or more) threads try to acquire
  // resources from eachother without releasing their own recources.
  // What happens is that the threads will wait for eachother to 
  // release the recources indefinately, since they're not releasing
  // their own.
  // It's just like waiting for CD project red to release Cyberpunk 2077


  // Deadlock implementation using lazy val
  object A {                            // Creating an object that has  two lazy values
    lazy val base = 42                  // in it, one called base, which has an int and
    lazy val start = B.step             // one called start which tries to acces a val in
  }                                     // another object

  object B {                            // This object houses the lazy val that A is trying
    lazy val step = A.base              // to access with the start val, and it leads to the 
  }                                     // base lazy val in A

  object Deadlock {
    def run = {
      val result = Future.sequence(Seq( // We initialize a sequence of moves, starting with
        Future { A.start },             // A.start. Since A.start is lazy, it tries to initialize
        Future { B.step }               // it's value, which is B.step. B.step is allso lazy, which 
      ))                                // means that it is not initialized until the next step in the
      Await.result(result, 1.minute)    // sequince, but the sequince cannot move on until A.start is 
    }                                   // initialized, creating a deadlock. The 1.minute timeout is 
  }                                     // there because the Await.result command requires there to be
}                                       // a timeout variable. The program crashes after it is timed out.