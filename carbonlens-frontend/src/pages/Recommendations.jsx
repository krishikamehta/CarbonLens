export default function Recommendations(){
  return(
    <div className="max-w-4xl mx-auto py-16">

      <h2 className="text-3xl font-bold mb-6">
        Recommended Actions
      </h2>

      <ul className="space-y-4">

        <li className="bg-green-100 p-4 rounded">
          Switch to public transport
        </li>

        <li className="bg-green-100 p-4 rounded">
          Reduce electricity usage by 20%
        </li>

        <li className="bg-green-100 p-4 rounded">
          Switch to vegetarian meals
        </li>

      </ul>

    </div>
  )
}