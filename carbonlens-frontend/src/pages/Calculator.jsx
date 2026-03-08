import { useState } from "react";
import { calculateFootprint } from "../api/api";

export default function Calculator() {

  const [data,setData] = useState({
    electricity_kwh:"",
    transport_mode:"petrol",
    transport_km:"",
    diet_type:"mixed",
    meals_per_month:"",
    waste_kg:""
  });

  const [result,setResult] = useState(null);

  const handleChange=(e)=>{
    setData({...data,[e.target.name]:e.target.value});
  }

  const submit=async()=>{
    const res=await calculateFootprint(data);
    setResult(res.data);
  }

  return(
    <div className="max-w-xl mx-auto py-12">

      <h2 className="text-2xl font-bold mb-6">Carbon Calculator</h2>

      <input
        name="electricity_kwh"
        placeholder="Electricity kWh"
        className="input"
        onChange={handleChange}
      />

      <input
        name="transport_km"
        placeholder="Transport km"
        className="input"
        onChange={handleChange}
      />

      <input
        name="meals_per_month"
        placeholder="Meals per month"
        className="input"
        onChange={handleChange}
      />

      <input
        name="waste_kg"
        placeholder="Waste kg"
        className="input"
        onChange={handleChange}
      />

      <button
        onClick={submit}
        className="bg-green-700 text-white px-6 py-2 mt-4 rounded"
      >
        Calculate
      </button>

      {result && (
        <div className="mt-6 bg-green-100 p-4 rounded">
          <p>Total CO₂: {result.total}</p>
        </div>
      )}

    </div>
  )
}