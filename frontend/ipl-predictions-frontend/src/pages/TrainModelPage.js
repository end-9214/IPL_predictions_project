import React, { useState } from "react";
import "./styles/TrainModelPage.css";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, Cell, ResponsiveContainer } from "recharts";

function TrainModelPage() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrainModel = async () => {
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/api/model-training/", {
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

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8884d8", "#82ca9d"];

  const renderNestedDetails = (data) => {
    return Object.entries(data).map(([key, value], index) => (
      <div key={index} className="nested-detail">
        <strong>{key.replace(/_/g, " ")}:</strong>{" "}
        {typeof value === "object" && value !== null ? (
          <div className="nested-detail-content">{renderNestedDetails(value)}</div>
        ) : (
          value.toString()
        )}
      </div>
    ));
  };

  const renderConfusionMatrixTable = (matrix) => {
    if (!matrix || matrix.length === 0) return null;
    
    const total = matrix.flat().reduce((sum, val) => sum + val, 0);
    
    const maxValue = Math.max(...matrix.flat());
    
    return (
      <div className="confusion-matrix-visualization">
        <table className="confusion-matrix">
          <tbody>
            <tr>
              <td className="matrix-header"></td>
              <td className="matrix-header">Predicted: Loss</td>
              <td className="matrix-header">Predicted: Win</td>
            </tr>
            <tr>
              <td className="matrix-header">Actual: Loss</td>
              <td 
                className="matrix-cell true-negative"
                style={{
                  backgroundColor: `rgba(0, 200, 0, ${matrix[0][0] / maxValue})`,
                  color: matrix[0][0] / maxValue > 0.5 ? '#fff' : '#000'
                }}
              >
                <div className="cell-value">{matrix[0][0]}</div>
                <div className="cell-percentage">({((matrix[0][0] / total) * 100).toFixed(1)}%)</div>
              </td>
              <td 
                className="matrix-cell false-positive"
                style={{
                  backgroundColor: `rgba(255, 100, 100, ${matrix[0][1] / maxValue})`,
                  color: matrix[0][1] / maxValue > 0.5 ? '#fff' : '#000'
                }}
              >
                <div className="cell-value">{matrix[0][1]}</div>
                <div className="cell-percentage">({((matrix[0][1] / total) * 100).toFixed(1)}%)</div>
              </td>
            </tr>
            <tr>
              <td className="matrix-header">Actual: Win</td>
              <td 
                className="matrix-cell false-negative"
                style={{
                  backgroundColor: `rgba(255, 100, 100, ${matrix[1][0] / maxValue})`,
                  color: matrix[1][0] / maxValue > 0.5 ? '#fff' : '#000'
                }}
              >
                <div className="cell-value">{matrix[1][0]}</div>
                <div className="cell-percentage">({((matrix[1][0] / total) * 100).toFixed(1)}%)</div>
              </td>
              <td 
                className="matrix-cell true-positive"
                style={{
                  backgroundColor: `rgba(0, 200, 0, ${matrix[1][1] / maxValue})`,
                  color: matrix[1][1] / maxValue > 0.5 ? '#fff' : '#000'
                }}
              >
                <div className="cell-value">{matrix[1][1]}</div>
                <div className="cell-percentage">({((matrix[1][1] / total) * 100).toFixed(1)}%)</div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div className="matrix-legend">
          <div className="legend-item">
            <span className="legend-color true-positive-legend"></span>
            <span>True Positive: Correctly predicted Win</span>
          </div>
          <div className="legend-item">
            <span className="legend-color true-negative-legend"></span>
            <span>True Negative: Correctly predicted Loss</span>
          </div>
          <div className="legend-item">
            <span className="legend-color false-positive-legend"></span>
            <span>False Positive: Incorrectly predicted Win</span>
          </div>
          <div className="legend-item">
            <span className="legend-color false-negative-legend"></span>
            <span>False Negative: Incorrectly predicted Loss</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="page">
      <h1 className="title">IPL Match Prediction Model Training</h1>
      <button className="fetch-button" onClick={handleTrainModel} disabled={loading}>
        {loading ? "Training..." : "Train Model"}
      </button>

      {loading && (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>Training the model, please wait...</p>
        </div>
      )}

      {response && !loading && (
        <div className="content">
          {response.error ? (
            <p className="error-message">Error: {response.error}</p>
          ) : (
            <div>
              <h2 className="success-message">{response.message}</h2>
              {response.output?.accuracy && (
                <div className="accuracy-badge">
                  Model Accuracy: {(response.output.accuracy * 100).toFixed(2)}%
                </div>
              )}

              <div className="results-card">
                <h3 className="section-title">Confusion Matrix</h3>
                {response.output?.confusion_matrix ? (
                  <div className="confusion-matrix-container">
                    <p className="matrix-explanation">
                      {response.insights?.model_evaluation_analysis?.confusion_matrix?.explanation || 
                       "This confusion matrix shows how the model performed across different prediction outcomes."}
                    </p>
                    {renderConfusionMatrixTable(response.output.confusion_matrix)}
                  </div>
                ) : (
                  <p>Confusion matrix data is not available.</p>
                )}
              </div>

              <div className="results-card">
                <h3 className="section-title">Feature Importance</h3>
                {response.output?.feature_importance ? (
                  <div className="chart-container">
                    <ResponsiveContainer width="100%" height={400}>
                      <BarChart
                        data={response.output.feature_importance.slice().sort((a, b) => b.importance - a.importance)}
                        margin={{ top: 20, right: 30, left: 20, bottom: 70 }}
                      >
                        <XAxis 
                          dataKey="feature" 
                          angle={-45} 
                          textAnchor="end"
                          height={80}
                          interval={0}
                          tick={{ fontSize: 12 }}
                        />
                        <YAxis 
                          label={{ value: 'Importance', angle: -90, position: 'insideLeft', style: { textAnchor: 'middle' } }}
                        />
                        <Tooltip formatter={(value) => [value.toFixed(4), "Importance"]} />
                        <Legend />
                        <Bar dataKey="importance" name="Feature Importance" fill="#8884d8">
                          {response.output.feature_importance.map((entry, index) => (
                            <Cell
                              key={`cell-${index}`}
                              fill={COLORS[index % COLORS.length]}
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <p>Feature importance data is not available.</p>
                )}
              </div>

              <div className="results-card">
                <h3 className="section-title">Classification Report</h3>
                {response.output?.classification_report ? (
                  <div className="classification-grid">
                    {Object.entries(response.output.classification_report)
                      .filter(([key]) => !['accuracy', 'macro avg', 'weighted avg'].includes(key))
                      .map(([key, value]) => (
                        <div key={key} className="classification-section">
                          <h4>{key === "0" ? "Loss" : key === "1" ? "Win" : key.toUpperCase()}</h4>
                          {typeof value === "object" && (
                            <>
                              <p><strong>Precision:</strong> {value.precision.toFixed(2)}</p>
                              <p><strong>Recall:</strong> {value.recall.toFixed(2)}</p>
                              <p><strong>F1-score:</strong> {value['f1-score'].toFixed(2)}</p>
                              <p><strong>Support:</strong> {value.support}</p>
                            </>
                          )}
                        </div>
                      ))}
                    
                    {Object.entries(response.output.classification_report)
                      .filter(([key]) => ['macro avg', 'weighted avg'].includes(key))
                      .map(([key, value]) => (
                        <div key={key} className="classification-section">
                          <h4>{key.toUpperCase()}</h4>
                          {typeof value === "object" && (
                            <>
                              <p><strong>Precision:</strong> {value.precision.toFixed(2)}</p>
                              <p><strong>Recall:</strong> {value.recall.toFixed(2)}</p>
                              <p><strong>F1-score:</strong> {value['f1-score'].toFixed(2)}</p>
                              <p><strong>Support:</strong> {value.support}</p>
                            </>
                          )}
                        </div>
                      ))}
                      
                    {response.output.classification_report.accuracy && (
                      <div className="classification-section">
                        <h4>OVERALL ACCURACY</h4>
                        <p><strong>Accuracy:</strong> {response.output.classification_report.accuracy.toFixed(2)}</p>
                      </div>
                    )}
                  </div>
                ) : (
                  <p>Classification report data is not available.</p>
                )}
              </div>

              <div className="results-card">
                <h3 className="section-title">Model Insights</h3>
                {response.insights ? (
                  <div className="insight-section">
                    {Object.entries(response.insights).map(([key, value], index) => (
                      <div key={index} className="insight-card">
                        <h4>{key.replace(/_/g, " ").toUpperCase()}</h4>
                        {renderNestedDetails(value)}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p>Insights data is not available.</p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default TrainModelPage;