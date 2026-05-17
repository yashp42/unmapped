import React from "react";

export default function LoadingSpinner({ size = 24 }) {
  return (
    <div style={{ width: size, height: size }} className="inline-block">
      <svg className="animate-spin" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="rgba(0,0,0,0.12)" strokeWidth="4" />
        <path d="M22 12a10 10 0 00-10-10" stroke="currentColor" strokeWidth="4" strokeLinecap="round" />
      </svg>
    </div>
  );
}
