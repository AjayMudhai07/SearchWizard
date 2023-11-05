import React, { useState, useRef } from 'react';
import './HomePage.css';

// Define the path to the shared icon for follow-up questions outside the component
const sharedIconPath = '/enter.png'; // Update this path to your icon's location

const FollowUpQuestions = ({ followUpQuestions, onQuestionSelect }) => {
  const scrollContainerRef = useRef(null);
  
  // Function to scroll the questions left or right
  const scroll = (scrollOffset) => {
    scrollContainerRef.current.scrollLeft += scrollOffset;
  };

  // Handler when a follow-up question is selected
  const handleQuestionClick = (questionText) => {
    onQuestionSelect(questionText);
  };

  return (
    <div className="follow-up-container">
      <button onClick={() => scroll(-100)} className="scroll-btn left">&lt;</button>
      <div className="questions-container" ref={scrollContainerRef}>
        {followUpQuestions.map((question, index) => (
          <button key={index} className="question-btn" onClick={() => handleQuestionClick(question.text)}>
            <img src={sharedIconPath} alt="Q" className="question-icon" />
            {question.text}
          </button>
        ))}
      </div>
      <button onClick={() => scroll(100)} className="scroll-btn right">&gt;</button>
      <div className="searchContainer">
            <input type="text" className="searchInput" placeholder=""/>
            <div className="searchIconContainer">
                <img src="/sendIcon.png" alt="Send" className="searchIcon" />
            </div>
      </div>
    </div>
  );
};

export default FollowUpQuestions;
