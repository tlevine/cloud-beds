(ns my-app.core
  (:require [clj-http.client :as client]))

(use 'environ.core)

(def aws-creds
  {:access-key (env :aws-access-key)
   :secret-key (env :aws-secret-key)})

(client/get "http://google.com")

    val APIKEY = scala.util.Properties.envOrElse("APIKEY", "")

//  val svc = url(s"http://search.3taps.com?auth_token=$APIKEY&location.state=USA-NY&category=RSUB")
//  val country = Http(svc OK as.String)
