import dispatch._
import dispatch.liftjson.Js._
import net.liftweb.json.JsonAST._
import scala.util.Properties

case class Device(device_token: String, alias: Option[String])

object download {
  def main(args: Array[String]) {
    val APIKEY = scala.util.Properties.envOrElse("APIKEY", "")

    val http = new Http()
    val u = url("http://gpodder.net/search.json") <<? Map("q" -> "scala")
    http(u ># { json => 
      (json \ "title" children) flatMap( _ match {
        case JField("title", JString(d)) => Some(d)
        case JString(d) => Some(d)
        case _ => None
      })
    })

//  val svc = url(s"http://search.3taps.com?auth_token=$APIKEY&location.state=USA-NY&category=RSUB")
//  val country = Http(svc OK as.String)
  }
}
