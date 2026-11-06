import type { CSSProperties } from "react";

interface LogoProps {
  size?: number;
  onDark?: boolean;
}

export default function Logo({
  size = 18,
  onDark = false,
}: LogoProps) {
  const style: CSSProperties = {
    height: `${Math.round(size * 1.35)}px`,
    width: "auto",
    objectFit: "contain",
    filter: onDark ? "brightness(0) invert(1)" : undefined,
  };

  return (
    <img
      src="/hireforce-logo.svg"
      alt="HireForce"
      style={style}
    />
  );
}
