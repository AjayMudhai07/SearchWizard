import React, { useState } from 'react';
import Draggable from 'react-draggable';
import { Resizable } from 'react-resizable';
import './App.css';

const ImageGrid = ({ images }) => {
  const [isResizeActive, setIsResizeActive] = useState(false);
  const [draggableIndex, setDraggableIndex] = useState(null);

  const handleDragStart = (index) => {
    setDraggableIndex(index);
  };

  const handleDragStop = () => {
    setDraggableIndex(null);
  };

  return (
    <div className="image-grid">
      {images.map((src, index) => (
        <Draggable 
          disabled={draggableIndex !== index}
          key={index}
          onStop={handleDragStop}
        >
          <Resizable width={200} height={200} disabled={!isResizeActive}>
            <div className="image-wrapper">
              <div className="control-icons">
                <img 
                  src="/Draggable-icon.png" 
                  alt="Dragging" 
                  onMouseDown={() => handleDragStart(index)} 
                  onMouseUp={handleDragStop}
                />
                {/* <img 
                  src="/Resizeable-icon.png" 
                  alt="Resizing" 
                  onClick={() => setIsResizeActive(!isResizeActive)} 
                /> */}
              </div>
              <img src={src} alt={`Dynamic Img ${index}`} className="dynamic-image" />
            </div>
          </Resizable>
        </Draggable>
      ))}
    </div>
  );
};

export default ImageGrid;
