export default function FeatureCard({title,description}) {
  return (
    <div className="bg-white shadow rounded-lg p-6 hover:shadow-lg transition">
      <h3 className="font-semibold text-lg mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}