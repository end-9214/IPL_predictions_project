import React, { useState } from "react";
import "./styles/CurrentPredictionsPage.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer
} from "recharts";

function CurrentPredictionsPage() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCurrentPredictions = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/api/current-predictions/", {
        method: "GET",
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data = await res.json();
      console.log("API Response:", data);
      setResponse(data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
      setResponse({ error: error.message });
      setLoading(false);
    }
  };

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042"];

  const renderCustomLabel = ({ name, value }) => {
    return `${name}: ${value}%`;
  };

  const renderMatchDetails = (matchData) => {
    return Object.entries(matchData).map(([key, value], index) => (
      <div key={index} className="match-detail">
        <strong>{key.replace(/_/g, " ")}:</strong>{" "}
        {typeof value === "object" && value !== null ? (
          <div className="nested-detail">
            {renderMatchDetails(value)}
          </div>
        ) : (
          value.toString()
        )}
      </div>
    ));
  };

  return (
    <div className="page">
      <h1 className="title">Current IPL Match Predictions</h1>
      <button className="fetch-button" onClick={handleCurrentPredictions} disabled={loading}>
        {loading ? "Loading Predictions..." : "Get Today's Predictions"}
      </button>

      {loading && (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Fetching predictions, please wait...</p>
        </div>
      )}

      {response && !loading && (
        <div className="content">
          {response.error ? (
            <p className="error-message">Error: {response.error}</p>
          ) : (
            <div>
              <h2 className="section-title">Match Predictions</h2>
              {response.predictions &&
                response.predictions.map((prediction, index) => (
                  <div key={index} className="prediction-card">
                    <h3>
                      {prediction.team1} vs {prediction.team2}
                    </h3>
                    <p>
                      <strong>Venue:</strong> {prediction.venue}
                    </p>
                    <p>
                      <strong>City:</strong> {prediction.city}
                    </p>

                    <div className="visualization-container">
                      <div className="chart">
                        <h4>Team Win Rates</h4>
                        <ResponsiveContainer width={300} height={250}>
                          <BarChart
                            data={[
                              {
                                name: prediction.team1,
                                WinRate: (prediction.team1_win_rate * 100).toFixed(2),
                              },
                              {
                                name: prediction.team2,
                                WinRate: (prediction.team2_win_rate * 100).toFixed(2),
                              },
                            ]}
                          >
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="WinRate" fill="#007bff" />
                          </BarChart>
                        </ResponsiveContainer>
                      </div>

                      <div className="chart">
                        <h4>Toss Outcome Probabilities</h4>
                        <ResponsiveContainer width={300} height={250}>
                          <PieChart>
                            <Pie
                              data={prediction.toss_outcomes.map((outcome, idx) => ({
                                name: `${outcome.toss_winner} (${outcome.toss_decision})`,
                                value: outcome.winning_probability,
                              }))}
                              cx="50%"
                              cy="50%"
                              outerRadius={100}
                              fill="#8884d8"
                              dataKey="value"
                              label={renderCustomLabel}
                            >
                              {prediction.toss_outcomes.map((_, idx) => (
                                <Cell key={`cell-${idx}`} fill={COLORS[idx % COLORS.length]} />
                              ))}
                            </Pie>
                            <Tooltip />
                          </PieChart>
                        </ResponsiveContainer>
                      </div>
                    </div>

                    <h4>Detailed Toss Outcomes</h4>
                    <ul className="toss-list">
                      {prediction.toss_outcomes.map((outcome, idx) => (
                        <li key={idx}>
                          <strong>Toss Winner:</strong> {outcome.toss_winner}{" "}
                          <strong>Decision:</strong> {outcome.toss_decision}{" "}
                          <strong>Predicted Winner:</strong> {outcome.predicted_winner}{" "}
                          <strong>Winning Probability:</strong> {outcome.winning_probability}%
                        </li>
                      ))}
                    </ul>

                    <h4>Prediction Summary</h4>
                    <p>
                      Based on the analysis, the predicted winner is{" "}
                      <strong>
                        {
                          prediction.toss_outcomes.reduce((prev, current) =>
                            prev.winning_probability > current.winning_probability
                              ? prev
                              : current
                          ).predicted_winner
                        }
                      </strong>
                    </p>
                  </div>
                ))}

              <h2 className="section-title">Analysis Insights</h2>
              {response.insights ? (
                Object.keys(response.insights).map((key, index) => (
                  <div key={index} className="insight-card">
                    <h3>{key.replace(/_/g, " ").toUpperCase()}</h3>
                    {renderMatchDetails(response.insights[key])}
                  </div>
                ))
              ) : (
                <p>No insights available.</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default CurrentPredictionsPage;