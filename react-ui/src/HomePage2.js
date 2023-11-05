import React, { useState } from 'react';
import UserQuestion from './UserQuestion';
import AnswerSection from './AnswerSection'; // Import the AnswerSection component you created
import FollowUpQuestions from './FollowUpQuestions'; // Import the FollowUpQuestions component
// import profilePic from './profile.png'; // Path to your profile image

// Mock data for follow-up questions (You would replace this with your actual API data)
const mockFollowUpQuestions = [
    { text: 'Follow-up Question 1' },
    { text: 'Follow-up Question 2' },
    { text: 'Follow-up Question 1' },
    { text: 'Follow-up Question 2' },
    { text: 'Follow-up Question 1' },
    { text: 'Follow-up Question 2' },
    { text: 'Follow-up Question 1' },
    { text: 'Follow-up Question 2' },
    { text: 'Follow-up Question 1' },
    { text: 'Follow-up Question 2' },
    // Add more follow-up question text here
  ];

const HomePage2 = () => {
    // Example question
    const userQuestion = "Customers who placed orders more than $1000";
    const answerData = {
        answerText: "Total numbers of customers with order > 1000 = 2134",
        graphImage: '/graph-answer.png', // The path to the graph image file
        insightText: 'Loans Revenue Rate Insights Report' +
        'Report Date: October 4, 2023 ' +
        'The profitability of loan portfolios.In Q1-Q4 2023, the industry average loans revenue rate stood at 8.2%.',
      };
      

    // Example function to simulate the export action
    const handleExport = () => {
        console.log("Exporting graph...");
        // Implement the function to export the graph
    };

    // Example function to simulate adding graph to dashboard
    const handleAddToDashboard = () => {
        console.log("Adding graph to dashboard...");
        // Implement the function to add the graph to the dashboard
    };

    return (
        <div className='HomePage2Container'>
            <UserQuestion profileImage={"/profile.png"} question={userQuestion} />
            <AnswerSection
                answerData={answerData}
                onExport={handleExport}
                onAddToDashboard={handleAddToDashboard}
            />
            <FollowUpQuestions followUpQuestions={mockFollowUpQuestions} />
            {/* ... other components or content ... */}
        </div>
    );
};

export default HomePage2;
