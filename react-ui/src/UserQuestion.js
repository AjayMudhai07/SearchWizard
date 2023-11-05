import React from 'react';
import './HomePage2.css';

const UserQuestion = ({ profileImage, question }) => {
    return (
        <div className="userQuestionContainer">
            <img src={profileImage} alt="User" className="profileImage" />
            <div className="questionBox">{question}</div>
        </div>
    );
};

export default UserQuestion;
