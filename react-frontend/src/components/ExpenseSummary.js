import React from "react";

const ExpenseSummary = ({ classification }) => {
  if (!classification) return null;

  const total = Object.values(classification).reduce(
    (sum, value) => sum + value,
    0
  );

  return (
    <div className="expense-summary">
      <h3>Detailed Expense Summary</h3>
      <ul>
        {Object.keys(classification).map((category) => (
          <li key={category}>
            <strong>{category}</strong>: ${classification[category].toFixed(2)}
          </li>
        ))}
      </ul>
      <p className="total-expense">
        <strong>Total:</strong> ${total.toFixed(2)}
      </p>
    </div>
  );
};

export default ExpenseSummary;
