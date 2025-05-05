import React, { useState } from "react";
import "./styles/UploadMatchesPage.css"; 
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";

function UploadMatchesPage() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const entriesPerPage = 10;

  const handleUploadMatches = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/api/upload-matches/", {
        method: "GET",
      });
      const data = await res.json();
      setResponse(data);
      setLoading(false);
    } catch (error) {
      setResponse({ error: error.message });
      setLoading(false);
    }
  };

  const indexOfLastEntry = currentPage * entriesPerPage;
  const indexOfFirstEntry = indexOfLastEntry - entriesPerPage;
  const currentEntries =
    response && response.matches
      ? response.matches.slice(indexOfFirstEntry, indexOfLastEntry)
      : [];

  const handleNextPage = () => {
    if (response && currentPage < Math.ceil(response.matches.length / entriesPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="page">
      <h1 className="title">Upload Matches Dataset</h1>
      <button className="fetch-button" onClick={handleUploadMatches} disabled={loading}>
        {loading ? "Uploading..." : "Upload Matches"}
      </button>

      {loading && (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Uploading matches, please wait...</p>
        </div>
      )}

      {response && !loading && (
        <div className="content">
          {response.error ? (
            <p className="error-message">Error: {response.error}</p>
          ) : (
            <div>
              <h2 className="success-message">{response.message}</h2>

              <h3 className="section-title">Uploaded Matches</h3>
              <div className="matches-table-container">
                <table className="matches-table">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Team 1</th>
                      <th>Team 2</th>
                      <th>Venue</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentEntries.map((match, index) => (
                      <tr key={index}>
                        <td>{match.date}</td>
                        <td>{match.team1}</td>
                        <td>{match.team2}</td>
                        <td>{match.venue}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                <div className="pagination">
                  <button
                    className="pagination-button"
                    onClick={handlePreviousPage}
                    disabled={currentPage === 1}
                  >
                    Previous
                  </button>
                  <span className="pagination-info">
                    Page {currentPage} of{" "}
                    {response ? Math.ceil(response.matches.length / entriesPerPage) : 1}
                  </span>
                  <button
                    className="pagination-button"
                    onClick={handleNextPage}
                    disabled={
                      response &&
                      currentPage === Math.ceil(response.matches.length / entriesPerPage)
                    }
                  >
                    Next
                  </button>
                </div>
              </div>

              <h3 className="section-title">Team Win Rates - Home vs Away</h3>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart
                    data={response.winrates.map((winrate) => ({
                      team: winrate.team,
                      Home: parseFloat(winrate.home_win_percentage),
                      Away: parseFloat(winrate.away_win_percentage),
                    }))}
                    margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
                  >
                    <XAxis 
                      dataKey="team" 
                      angle={-45} 
                      textAnchor="end" 
                      height={80}
                      interval={0}
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis 
                      label={{ 
                        value: 'Win Percentage (%)', 
                        angle: -90, 
                        position: 'insideLeft',
                        style: { textAnchor: 'middle' } 
                      }}
                    />
                    <Tooltip formatter={(value) => `${value.toFixed(2)}%`} />
                    <Legend />
                    <Bar dataKey="Home" fill="#8884d8" name="Home Win %" />
                    <Bar dataKey="Away" fill="#82ca9d" name="Away Win %" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default UploadMatchesPage;