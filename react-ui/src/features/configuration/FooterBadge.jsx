import React from "react";
const addIcon = "/add.png";

const FooterBadge = ({ title, image, description }) => {
  return (
    <div className="flex items-center justify-between px-5 py-3 bg-white rounded-lg">
      <div className="flex items-center gap-5">
        <img src={image} alt={title} height={28} width={28} />
        <div className="flex flex-col">
          <h5 className="text-xl font-semibold ">{title}</h5>
          <p className="text-xl font-normal">{description}</p>
        </div>
      </div>
      <img src={addIcon} alt="add" height={28} width={28} />
    </div>
  );
};

export default FooterBadge;