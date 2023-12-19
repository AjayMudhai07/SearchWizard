import React, { useState } from "react";

const MerchantId = (props) => {
  const [merchantId, setMerchantId] = useState("#12345678");
  const [isEditing, setIsEditing] = useState(true);

  const handleInputChange = (event) => {
    setMerchantId(event.target.value);
  };

  const handleInputKeyDown = (event) => {
    if (event.key === "Enter") {
      setIsEditing(false); // Exit editing mode
      props.onChange(merchantId);
      console.log("Merchant ID saved:", merchantId); // For demonstration purposes
    }
  };

  const handleEditClick = () => {
    setIsEditing(true); // Enter editing mode
  };

  return (
    <div className="flex gap-2">
      <label className="text-2xl font-bold whitespace-nowrap" htmlFor="merchantId">
        Merchant Id:
      </label>
      {isEditing ? (
        <input
          className="px-3 py-1 border rounded-md outline-none"
          id="merchantId"
          type="text"
          value={merchantId}
          onChange={handleInputChange}
          onKeyDown={handleInputKeyDown}
          autoFocus
        />
      ) : (
        <div className="merchant-id-display" onClick={handleEditClick}>
          {merchantId}
        </div>
      )}
    </div>
  );
};

export default MerchantId;
