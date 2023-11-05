import React from 'react';
import './index.css';

function Dashboard({ optionName }) {
    return (
        <div className="dashboard">
            <div className="search-bar">
                <div className="search-icon">
                    <img src="/search.png" alt="Search Icon" />
                </div>
                <input type="text" placeholder="Add new metric to this dashboard" className="search-input" />
            </div>
            <div className="dashboard-name">{optionName}</div>
        </div>
    );
}

export default Dashboard;
