import {useEffect,useState} from "react"
import {getHistory} from "../api/footprint"

export default function History(){

const user = JSON.parse(localStorage.getItem("user"))

const [data,setData]=useState([])

useEffect(()=>{

if(user){
getHistory(user.email).then(res=>setData(res.data))
}

},[])

return(

<div className="p-10">

<h2 className="text-2xl font-bold mb-6">
Your Footprint History
</h2>

{data.map(d=>(

<div key={d.id} className="bg-white p-4 shadow mb-3">

Total footprint: {d.total}

</div>

))}

</div>

)

}