import React from 'react';

function MainComponent({ optionName }) {
  return (
    <main>
      <div className="container">
        <p>Content for {optionName} will go here.</p>
      </div>
      <div className="graphs-container">
        {/* {Array.from({ length: 4 }, (_, i) => (
          <div key={i} className="graph-section">
            <img src={`/graph${i + 1}.png`} alt={`Graph ${i + 1}`} />
          </div>
        // ))} */}
      </div>
    </main>
  );
}

export default MainComponent;
