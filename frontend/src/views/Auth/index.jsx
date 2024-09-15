import { useLocation, Redirect } from "wouter";
import useSWR from "swr";

function parseQueryString () {
  var str=window.location.search
  var objUrl={}
  str.replace(
    new RegExp("([^?=&]+)(=([^&]*))?","g"),
    function ($0,$1,$2,$3){
      objUrl[$1]=$3;
    }
  )
  return objUrl
}

function setSession (value){
  localStorage.setItem("sessionId",value)
}

function fetchSession() {
  return localStorage.getItem("sessionId")
}
export default function RequireSession({children}){
  let params=parseQueryString()
  if (params.sessionId){
    setSession(params.sessionId)
    window.history.replaceState(null, null, "/")
  } else {
    let auth = fetchSession()
    const [location,setLocation] = useLocation()
    const fetcher = (...args) => fetch(...args,{redirect:"follow"}).then((res) =>{if(res.redirected){window.location.href=res.url} else {return res.json()}});
    const { data, error, isLoading } = useSWR("/api/auth?sessionId="+auth, fetcher);
  }
  return children;
}