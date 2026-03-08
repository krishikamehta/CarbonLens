import { PieChart, Pie, Cell, Tooltip } from "recharts";

const COLORS = ["#2E7D32", "#66BB6A", "#A5D6A7", "#C8E6C9"];

export default function EmissionChart({ data }) {

  const chartData = [
    { name: "Electricity", value: data.electricity },
    { name: "Transport", value: data.transport },
    { name: "Food", value: data.food },
    { name: "Waste", value: data.waste }
  ];

  return (
    <PieChart width={350} height={300}>
      <Pie
        data={chartData}
        dataKey="value"
        outerRadius={100}
        label
      >
        {chartData.map((entry, index) => (
          <Cell key={index} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>

      <Tooltip />
    </PieChart>
  );
}