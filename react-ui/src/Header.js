import React from 'react';

function DashboardHeader() {
    return (
        <div className="header">
            <div className="top-right-logos">
                <div className="right-logo-container">
                    <img src="/i1.png" className="right-logo-1" alt="Icon A2" />
                </div>
                <div className="right-logo-container">
                    <img src="/i2.png" className="right-logo-2" alt="Icon B2" />
                </div>
                <div className="right-logo-container">
                    <img src="/i3.png" className="right-logo-3" alt="Icon C2" />
                </div>
            </div>
            <div className="dashboard-heading-container">
                <h1>Data visualisation board</h1>
                <p>Customise the visual data as you like!</p>
            </div>
        </div>
    );
}

export default DashboardHeader;
