open class Wheel
{

  public var diameter: Int
  init
  {
    diameter = 3
  }

  open fun type() : String { return "Wheel" }


}

class RoadWheel : Wheel()
{
  override fun type() : String { return "RoadWheel" }
}

class CrossWheel : Wheel()
{
  override fun type() : String { return "CrossWheel" }
}

fun nullable(a: Int?): Int? {
  if(a != null)
  {
    return a
  }
  return null;
}

fun double(n: Int) : Int {
  return n*2
}

fun looping() {
  for(i in 1..10 step 2)
  {
    println("For looping : "+i)
  }
}

fun polymorphism()
{
  var wheels = listOf(CrossWheel(), RoadWheel())
  for(wheel in wheels)
  {
    println(wheel.type())
  }
}

fun map()
{
  var x = 9
  var t = 3
  var ret = when(t)
  {
    1 -> double(1)
    3 -> double(x)
    else -> null
  }

  println("map:"+ret)
}

fun lambda()
{
  var a : Int = 3
  var b = {
    param : Int -> Int
    param*9
  }
  println(b(a))
}

fun main(args: Array<String>) {
  listOf(1,2,3).filter{ it > 0 }.forEach{println(it)}
  println(double(3))
  looping()
  var list = listOf(2, null)
  for(l in list)
  {
    println("Calling nullable with "+l);
    println(nullable(l))
  }
  polymorphism()

  map()
  lambda()
}
