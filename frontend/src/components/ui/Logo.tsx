import React from "react";

interface LogoProps {
  className?: string;
  dark?: boolean;
}

const Logo: React.FC<LogoProps> = ({ className = "", dark = false }) => (
  <div className={`flex items-center gap-2 ${className}`}>
    <img
      src="/hireforce-logo.svg"
      alt="HireForce Logo"
      width="34"
      height="34"
      style={{ filter: dark ? "brightness(0) invert(1)" : "none" }}
    />
    <span
      className={`font-bold text-lg tracking-tight ${dark ? "text-white" : "text-slate-900"}`}
    >
      HireForce
    </span>
  </div>
);

export default Logo;
