import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./lib/auth";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import Explore from "./pages/Explore";
import TrackPage from "./pages/TrackPage";
import AlbumUniverse from "./pages/AlbumUniverse";
import ConnectionMap from "./pages/ConnectionMap";
import VibesIndex from "./pages/VibesIndex";
import VibePage from "./pages/VibePage";
import LoreIndex from "./pages/LoreIndex";
import LoreEntry from "./pages/LoreEntry";
import TheoriesIndex from "./pages/TheoriesIndex";
import TheoryPage from "./pages/TheoryPage";
import ContributorsIndex from "./pages/ContributorsIndex";
import ContributorProfile from "./pages/ContributorProfile";
import MyWorld from "./pages/MyWorld";
import Login from "./pages/Login";
import Register from "./pages/Register";
import SearchPage from "./pages/SearchPage";

function Shell({ children }) {
  return (
    <div className="App">
      <Header />
      <main className="min-h-[60vh]">{children}</main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Shell><Home /></Shell>} />
          <Route path="/explore" element={<Shell><Explore /></Shell>} />
          <Route path="/track/:id" element={<Shell><TrackPage /></Shell>} />
          <Route path="/album/:id" element={<Shell><AlbumUniverse /></Shell>} />
          <Route path="/connections" element={<Shell><ConnectionMap /></Shell>} />
          <Route path="/vibes" element={<Shell><VibesIndex /></Shell>} />
          <Route path="/vibe/:id" element={<Shell><VibePage /></Shell>} />
          <Route path="/lore" element={<Shell><LoreIndex /></Shell>} />
          <Route path="/lore/:id" element={<Shell><LoreEntry /></Shell>} />
          <Route path="/theories" element={<Shell><TheoriesIndex /></Shell>} />
          <Route path="/theory/:id" element={<Shell><TheoryPage /></Shell>} />
          <Route path="/contributors" element={<Shell><ContributorsIndex /></Shell>} />
          <Route path="/c/:handle" element={<Shell><ContributorProfile /></Shell>} />
          <Route path="/my-world" element={<Shell><MyWorld /></Shell>} />
          <Route path="/search" element={<Shell><SearchPage /></Shell>} />
          <Route path="/login" element={<Shell><Login /></Shell>} />
          <Route path="/register" element={<Shell><Register /></Shell>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
