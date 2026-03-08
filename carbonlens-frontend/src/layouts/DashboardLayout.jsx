import Sidebar from "../components/Sidebar";

export default function DashboardLayout({children}){

  return(
    <div className="flex">

      <Sidebar />

      <div className="flex-1 p-8 bg-gray-50 min-h-screen">
        {children}
      </div>

    </div>
  );
}