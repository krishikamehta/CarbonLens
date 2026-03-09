import { useState } from "react";
import { registerUser } from "../api/auth";
import { useNavigate } from "react-router-dom";

export default function Signup(){

  const navigate = useNavigate();

  const [form,setForm] = useState({
    name:"",
    email:"",
    password:""
  });

  const handleChange=(e)=>{
    setForm({...form,[e.target.name]:e.target.value});
  };

  const handleSignup=async()=>{

    try{

      await registerUser(form);

      alert("Account created");

      navigate("/login");

    }catch(err){

      alert("Signup failed");

    }

  };

  return(

  <div className="flex items-center justify-center h-screen">

    <div className="bg-white p-8 shadow rounded w-96">

      <h2 className="text-2xl mb-6">Signup</h2>

      <input
      name="name"
      placeholder="Name"
      onChange={handleChange}
      className="w-full border p-2 mb-3"
      />

      <input
      name="email"
      placeholder="Email"
      onChange={handleChange}
      className="w-full border p-2 mb-3"
      />

      <input
      name="password"
      type="password"
      placeholder="Password"
      onChange={handleChange}
      className="w-full border p-2 mb-3"
      />

      <button
      onClick={handleSignup}
      className="w-full bg-green-600 text-white py-2 rounded"
      >
      Signup
      </button>

    </div>

  </div>

  );

}