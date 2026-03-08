export default function FootprintCard({ result }) {

  return (
    <div className="bg-green-50 p-6 rounded-lg shadow-md mt-6">

      <h3 className="text-xl font-semibold mb-4">
        Carbon Footprint Results
      </h3>

      <div className="space-y-2">

        <p>Electricity: {result.electricity.toFixed(2)} kg CO₂</p>
        <p>Transport: {result.transport.toFixed(2)} kg CO₂</p>
        <p>Food: {result.food.toFixed(2)} kg CO₂</p>
        <p>Waste: {result.waste.toFixed(2)} kg CO₂</p>

        <hr />

        <p className="font-bold text-lg">
          Total: {result.total.toFixed(2)} kg CO₂
        </p>

      </div>

    </div>
  );
}