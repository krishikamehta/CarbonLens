import FeatureCard from "../components/FeatureCard";

export default function Home() {
  return (
    <div>

      {/* HERO */}
      <section className="bg-gradient-to-br from-green-900 via-green-700 to-green-500 text-white py-24 text-center">

        <h1 className="text-5xl font-bold">
          Understand Your Carbon Footprint
        </h1>

        <p className="mt-6 text-lg">
          Track emissions, simulate lifestyle changes,
          and discover impactful ways to reduce your footprint.
        </p>

      </section>

      {/* FEATURES */}
      <section className="max-w-6xl mx-auto grid md:grid-cols-3 gap-8 py-16">

        <FeatureCard
          title="Carbon Calculator"
          description="Estimate emissions from electricity, transport, food and waste."
        />

        <FeatureCard
          title="Scenario Simulator"
          description="Test lifestyle changes and measure carbon reduction."
        />

        <FeatureCard
          title="Smart Recommendations"
          description="Discover the most impactful carbon reduction actions."
        />

      </section>
    </div>
  );
}