libraryDependencies += 
  "net.databinder.dispatch" %% "dispatch-core" % "0.11.0"

libraryDependencies <++= (scalaVersion) { scalaVersion =>
  val liftVersion = scalaVersion match {
    case "2.10.2" => "2.5.1"
    case "2.9.1" | "2.9.2" => "2.4"
    case _ => "2.4-M2"
  }
  def sv(s: String) = s + "_" + (scalaVersion match {
      case "2.10.2" => "2.10"
      case "2.9.2" => "2.9.1"
      case v => v
  })
  Seq(
    "net.liftweb" % sv("lift-util") % liftVersion % "compile" intransitive(),
    "net.liftweb" % sv("lift-common") % liftVersion % "compile" intransitive(),
    "net.liftweb" % sv("lift-json") % liftVersion % "compile" intransitive())
}
