import { useState } from "react";
import { calculateFootprint } from "../api/footprint";

export default function Calculator() {

  const user = JSON.parse(localStorage.getItem("user"));

  const [electricity, setElectricity] = useState("");
  const [transportMode, setTransportMode] = useState("petrol");
  const [transportKm, setTransportKm] = useState("");
  const [dietType, setDietType] = useState("mixed");
  const [meals, setMeals] = useState("");
  const [waste, setWaste] = useState("");

  const [result, setResult] = useState(null);

  const handleCalculate = async () => {

    if (!user) {
      alert("Please login first");
      return;
    }

    const res = await calculateFootprint({
      name: user.name,
      email: user.email,
      electricity_kwh: Number(electricity),
      transport_mode: transportMode,
      transport_km: Number(transportKm),
      diet_type: dietType,
      meals_per_month: Number(meals),
      waste_kg: Number(waste)
    });

    setResult(res.data);
  };

  return (
    <div className="max-w-3xl mx-auto mt-10 p-6 bg-white shadow rounded">

      <h2 className="text-3xl font-bold mb-6">
        Carbon Footprint Calculator
      </h2>

      <div className="grid grid-cols-2 gap-4">

        <input
          placeholder="Electricity (kWh)"
          className="border p-2"
          value={electricity}
          onChange={(e) => setElectricity(e.target.value)}
        />

        <input
          placeholder="Transport km"
          className="border p-2"
          value={transportKm}
          onChange={(e) => setTransportKm(e.target.value)}
        />

        <select
          className="border p-2"
          value={transportMode}
          onChange={(e) => setTransportMode(e.target.value)}
        >
          <option value="petrol">Petrol</option>
          <option value="diesel">Diesel</option>
          <option value="public_transport">Public Transport</option>
        </select>

        <select
          className="border p-2"
          value={dietType}
          onChange={(e) => setDietType(e.target.value)}
        >
          <option value="veg">Veg</option>
          <option value="mixed">Mixed</option>
          <option value="non_veg">Non Veg</option>
        </select>

        <input
          placeholder="Meals per month"
          className="border p-2"
          value={meals}
          onChange={(e) => setMeals(e.target.value)}
        />

        <input
          placeholder="Waste (kg)"
          className="border p-2"
          value={waste}
          onChange={(e) => setWaste(e.target.value)}
        />

      </div>

      <button
        onClick={handleCalculate}
        className="mt-6 bg-green-600 text-white px-6 py-2 rounded"
      >
        Calculate
      </button>

      {result && (
        <div className="mt-6 bg-gray-100 p-4 rounded">

          <h3 className="text-xl font-bold mb-2">
            Results
          </h3>

          <p>Electricity: {result.electricity}</p>
          <p>Transport: {result.transport}</p>
          <p>Food: {result.food}</p>
          <p>Waste: {result.waste}</p>

          <p className="font-bold mt-2">
            Total: {result.total}
          </p>

        </div>
      )}

    </div>
  );
}