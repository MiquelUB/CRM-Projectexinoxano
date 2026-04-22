import { Sidebar } from "@/components/Sidebar";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-[#F4F7FB]">
      <Sidebar />
      <div className="flex-1 ml-72 flex flex-col min-h-screen">
        <main className="flex-1 p-10 max-w-[1600px] w-full mx-auto">
          {children}
        </main>
      </div>
    </div>
  );
}
