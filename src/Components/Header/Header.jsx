import React from "react";
import "../Header/Header.css";
import grainsens from "../../Images/grainsense.svg";
import YaMriy from "../../Images/YaMriy.svg";
import profilePhoto from "../../Images/profilePhoto.svg";
export function Header() {
  return (
    <header className="header">
      <div className="nav-bar">
        <div>
          <img className="grainsens" src={grainsens} alt="grainsens logo...." />
        </div>
        <div>
          <img className="YaMriy" src={YaMriy} alt="YaMriy logo....." />
        </div>
        <div className="profile">
          <p className="username">Username</p>
          <img src={profilePhoto} alt="Your avatar photo...." />
        </div>
      </div>
    </header>
  );
}
