"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface LandingViewProps {
  onButtonClick: (linkedinUrl: string) => void;
}

const LandingView: React.FC<LandingViewProps> = ({ onButtonClick }) => {
  const [inputValue, setInputValue] = useState("");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleSearch = () => {
    if (inputValue.trim()) {
      onButtonClick(inputValue.trim());
    }
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
        <motion.img
          src="/esther_orange.png"
          alt="Esther Orange"
          className="absolute bottom-14 left-14 w-60 h-60 pointer-events-none select-none object-cover "
          style={{ zIndex: 1 }}
          animate={{ rotate: [0, 15, -15, 0] }}
          transition={{
            duration: 6,
            repeat: Infinity,
            repeatType: "reverse",
            ease: "easeInOut",
          }}
        />
        <motion.img
          src="/esther_pink.png"
          alt="Esther Pink"
          className="absolute top-14 right-14 w-80 h-80 pointer-events-none select-none object-cover"
          style={{ zIndex: 1 }}
          animate={{ rotate: [0, -12, 12, 0] }}
          transition={{
            duration: 7,
            repeat: Infinity,
            repeatType: "reverse",
            ease: "easeInOut",
            delay: 1.5,
          }}
        />
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#FFE0D2] rounded-lg p-8">
          <h1 className="text-6xl font-semibold text-gray-900 mb-6 w-full text-left">
            Prospect, <br />
            <span className="font-light">With Your Eyes Closed.</span>
          </h1>

          <p className="text-xl text-[#7a7a7a] mb-12 w-full text-left font-light">
            s-esther is the{" "}
            <span className="font-medium">prospecting agent</span> that
            evaluates your lead's intent completely autonomously saving you{" "}
            <span className="font-medium">35% of your time</span> on research
            and intent validation.
          </p>

          <div className="w-full flex flex-col mb-8">
            <div className="p-2 flex flex-row justify-center items-center gap-2 max-w-[250px] bg-[#FFEFE8] border-2 border-b-0 border-dotted border-[#888888] rounded-sm font-light">
              ONE CLICK TO PROSPECT
              <img src="/cursor_img.png" alt="cursor" className="w-4 h-4" />
            </div>
            <div className="relative w-full">
              <img
                src="/search.png"
                alt="search"
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 z-10"
              />
              <Input
                value={inputValue}
                onChange={handleInputChange}
                placeholder="LinkedIn URL..."
                className="w-full h-16 font-light !text-md bg-white border-2 border-[#fff] rounded-sm mt-0 pl-12 pr-20"
              />
              <Button
                onClick={handleSearch}
                size="sm"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 h-12 px-8 rounded-[4px]"
              >
                Search
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingView;
