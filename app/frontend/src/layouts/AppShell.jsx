import Header from "../components/Header";
import Footer from "../components/Footer";

export default function AppShell({ children }) {
  return (
    <div className="App">
      <Header />
      <main className="min-h-[60vh]">{children}</main>
      <Footer />
    </div>
  );
}
