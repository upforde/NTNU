object Main {
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
  }

  // a) Function that takes in a body of code and returns a thread
  def thread(body: => Unit): Thread = {
    val t = new Thread {
      override def run() = body
    }
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

  
}