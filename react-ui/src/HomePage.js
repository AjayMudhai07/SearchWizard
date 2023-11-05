import NavBar from './NavBar';
import Header from './Header';
import { useState, useEffect } from 'react';
import React from 'react';
import './HomePage.css';

const HomePage = () => {
    return (
        <div className="whiteCard">
            <h1 className="mainHeading">Visual Analytics Engine</h1>

            <div className="cardsContainer">
                <Card 
                    icon="/home_i1.png"
                    heading="Connect data source"
                    text="The Romans used a type of ancient concrete called opus caementicium."
                />
                <Card 
                    icon="/home_i2.png"
                    heading="Analyse data"
                    text="The Romans used a type of ancient concrete called opus caementicium."
                />
                <Card 
                    icon="/home_i3.png"
                    heading="Visualise on dashboard"
                    text="The Romans used a type of ancient concrete called opus caementicium."
                />
            </div>

                <div className="searchContainer">
                    <input type="text" className="searchInput" placeholder=""/>
                    <div className="searchIconContainer">
                        <img src="/sendIcon.png" alt="Send" className="searchIcon" />
                    </div>
                </div>
        </div>
    );
};

const Card = ({ icon, heading, text }) => {
    return (
        <div className="card">
            <div className="circle">
                <img src={icon} alt={heading} className="cardIcon" />
            </div>
            <h2 className="cardHeading">{heading}</h2>
            <p className="cardText">{text}</p>
        </div>
    );
};

export default HomePage;
