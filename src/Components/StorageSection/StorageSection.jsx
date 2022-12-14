import React from "react";
import "../StorageSection/StorageSection.css";
import storagebottom from "../../Images/storagebottom.svg";
import house from "../../Images/grain_house.svg";
import dangerous_icon from "../../Images/dangerous_icon.svg";
import notification from "../../Images/notif_icon.svg";
import plus from "../../Images/plus.svg";
export function StorageSection() {
  return (
    <div className="storagesection">
      <div className="storage-section-text">
        <p className="username-hi">Hello bread</p>
        <p className="yourstorages">Your Storages</p>
      </div>
      <div className="storages">
        <div className="storage">
          <img
            className="notification"
            src={notification}
            alt="notification...."
          />
          <p className="storage-name">Ivan</p>
          <img
            className="dangerous_icon"
            src={dangerous_icon}
            alt="dangerous_icon...."
          />
          <div className="storage-photo">
            <img src={house} alt="house...." />
          </div>
          <img
            className="bottom-side"
            src={storagebottom}
            alt="storagebottom....."
          />
        </div>

        <div className="storage-add">
          <img className="plus" src={plus} />
        </div>
        <div className="instruction">
          <p>
            Є питання як користуватись? Відвідайте нашу сторінку з{" "}
            <a className="nub" href="https://www.w3schools.com/">
              <span className="someSpan"> інструкцією</span>
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
