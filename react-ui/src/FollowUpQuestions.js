import React, { useState, useRef } from "react";
import "./HomePage.css";

// Define the path to the shared icon for follow-up questions outside the component
const sharedIconPath = "/search.png"; // Update this path to your icon's location

const FollowUpQuestions = ({
  followUpQuestions,
  onQuestionSelect,
  handleSearchValue,
  onSearch,
}) => {
  const scrollContainerRef = useRef(null);
  const [inputValue, setInputValue] = useState("");

  // Function to scroll the questions left or right
  const scroll = (scrollOffset) => {
    scrollContainerRef.current.scrollLeft += scrollOffset;
  };

  // Handler when a follow-up question is selected
  const handleQuestionClick = (questionText) => {
    console.log(questionText);
    handleSearchValue(questionText)
      .then(() => {
        onSearch();
      })
      .catch((error) => {
        console.error("Error updating query:", error);
      });
    // onSearch();
  };

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
    handleSearchValue(event.target.value);
  };

  const handleKeyDown = (event) => {
    // Check if the Enter key was pressed
    if (event.key === "Enter") {
      onSearch();
    }
  };

  return (
    <>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <div className="searchContainer">
          <input
            type="text"
            className="searchInput"
            placeholder=""
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
          />
          <div className="searchIconContainer2">
            <img
              src="/sendIcon.png"
              alt="Send"
              className="searchIcon2"
              onClick={onSearch}
            />
          </div>
        </div>
      </div>
      <div className="follow-up-container">
        {/* <button onClick={() => scroll(-100)} className="scroll-btn left">
          &lt;
        </button> */}
        <div className="questions-container" ref={scrollContainerRef}>
          {followUpQuestions.map((question, index) => (
            <button
              key={index}
              className="question-btn"
              onClick={() => handleQuestionClick(question.text)}
            >
              <img src={sharedIconPath} alt="Q" className="question-icon" />
              {question.text}
            </button>
          ))}
        </div>
        {/* <button onClick={() => scroll(100)} className="scroll-btn right">
          &gt;
        </button> */}
      </div>
    </>
  );
};

export default FollowUpQuestions;
