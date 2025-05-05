import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import UploadMatchesPage from "./pages/UploadMatchesPage";
import CurrentPredictionsPage from "./pages/CurrentPredictionsPage";
import ManualDatePredictionsPage from "./pages/ManualDatePredictionsPage";
import TrainModelPage from "./pages/TrainModelPage";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<UploadMatchesPage />} />
        <Route path="/current-predictions" element={<CurrentPredictionsPage />} />
        <Route path="/manual-date-predictions" element={<ManualDatePredictionsPage />} />
        <Route path="/train-model" element={<TrainModelPage />} />
      </Routes>
    </Router>
  );
}

export default App;