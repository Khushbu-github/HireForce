/** HireForce wordmark with logo and slogan. */
export default function Logo({
  size = 18,
  onDark = false,
}: {
  size?: number;
  onDark?: boolean;
}) {
  const ink = onDark ? "var(--paper)" : "var(--ink)";
  const muted = onDark ? "rgba(240,246,255,0.65)" : "var(--muted)";
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
      <img
        src="/hireforce-logo.svg"
        alt="HireForce"
        style={{ height: size * 1.6, width: "auto" }}
        aria-hidden
      />
      <span style={{ display: "flex", flexDirection: "column", gap: 0 }}>
        <span
          style={{
            fontFamily: "var(--font-display)",
            fontWeight: 700,
            fontSize: size,
            letterSpacing: "-0.5px",
            color: ink,
            lineHeight: 1.1,
          }}
        >
          Hire<span style={{ color: "var(--signal-strong)" }}>Force</span>
        </span>
        <span
          style={{
            fontFamily: "var(--font-body)",
            fontWeight: 400,
            fontSize: size * 0.62,
            letterSpacing: "0.1px",
            color: muted,
            lineHeight: 1.2,
            whiteSpace: "nowrap",
          }}
        >
          Beyond Resumes. Beyond Expectations.
        </span>
      </span>
    </span>
  );
}
