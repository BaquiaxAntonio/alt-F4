import Sidebar from './Sidebar';
import Header from './Header';

export default function Layout({ children, openChat }) {
  return (
    <div className="flex bg-slate-50 font-body-md text-slate-900 antialiased min-h-screen">
      <Sidebar />
      <div className="pl-72 flex flex-col min-h-screen w-full">
        <Header openChat={openChat} />
        <main className="relative pt-16 flex-1 w-full bg-slate-50">
          <div className="flex flex-col w-full">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
