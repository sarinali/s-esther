import React from "react";

interface DottedGridProps {
  className?: string;
}

const DottedGrid: React.FC<DottedGridProps> = ({ className = "" }) => {
  return (
    <div className={`absolute inset-0 overflow-hidden bg-white ${className}`}>
      <div
        className="w-full h-full opacity-30"
        style={{
          backgroundImage: `
            radial-gradient(circle, #000 1.5px, transparent 1px)
          `,
          backgroundSize: "20px 20px",
          backgroundPosition: "0 0, 10px 10px",
        }}
      />
    </div>
  );
};

export default DottedGrid;
