import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./lib/auth";
import AppShell from "./layouts/AppShell";
import ProtectedRoute from "./components/ProtectedRoute";
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

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<AppShell><Home /></AppShell>} />
          <Route path="/explore" element={<AppShell><Explore /></AppShell>} />
          <Route path="/track/:id" element={<AppShell><TrackPage /></AppShell>} />
          <Route path="/album/:id" element={<AppShell><AlbumUniverse /></AppShell>} />
          <Route path="/connections" element={<AppShell><ConnectionMap /></AppShell>} />
          <Route path="/vibes" element={<AppShell><VibesIndex /></AppShell>} />
          <Route path="/vibe/:id" element={<AppShell><VibePage /></AppShell>} />
          <Route path="/lore" element={<AppShell><LoreIndex /></AppShell>} />
          <Route path="/lore/:id" element={<AppShell><LoreEntry /></AppShell>} />
          <Route path="/theories" element={<AppShell><TheoriesIndex /></AppShell>} />
          <Route path="/theory/:id" element={<AppShell><TheoryPage /></AppShell>} />
          <Route path="/contributors" element={<AppShell><ContributorsIndex /></AppShell>} />
          <Route path="/c/:handle" element={<AppShell><ContributorProfile /></AppShell>} />
          <Route
            path="/my-world"
            element={
              <AppShell>
                <ProtectedRoute>
                  <MyWorld />
                </ProtectedRoute>
              </AppShell>
            }
          />
          <Route path="/search" element={<AppShell><SearchPage /></AppShell>} />
          <Route path="/login" element={<AppShell><Login /></AppShell>} />
          <Route path="/register" element={<AppShell><Register /></AppShell>} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
