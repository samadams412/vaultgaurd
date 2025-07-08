import { useAuth } from "../context/AuthContext";


export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <>
      <div className="p-6">
        <h1 className="text-2xl font-bold">Welcome to the Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Logged in as: <span className="font-mono">{user?.email}</span>
        </p>
      </div>
    </>
  );
}
