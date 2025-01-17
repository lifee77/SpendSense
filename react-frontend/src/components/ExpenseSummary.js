import React from "react";

const ExpenseSummary = ({ classification }) => {
  if (!classification) return null;

  return (
    <div>
      <h3>Detailed Expense Summary</h3>
      <ul>
        {Object.keys(classification).map((category) => (
          <li key={category}>
            <strong>{category}</strong>: {classification[category].toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ExpenseSummary;
