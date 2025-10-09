"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface LandingViewProps {
  onButtonClick: (linkedinUrl: string, intent: string, dry_run: boolean) => void;
}

const LandingView: React.FC<LandingViewProps> = ({ onButtonClick }) => {
  const [inputValue, setInputValue] = useState("");
  const [intentValue, setIntentValue] = useState("Evaluate whether their company would like to buy a developer tool that does automated PR reviews targetted towards engineering heavy organizations...");

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleIntentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setIntentValue(e.target.value);
  };

  const handleSearch = () => {
    if (inputValue.trim()) {
      onButtonClick(inputValue.trim(), intentValue.trim(), false);
    }
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#FFE0D2]/40 rounded-md p-8 border-1 border-[#868686]">
          <h1 className="text-6xl font-semibold text-gray-900 mb-6 w-full text-left">
            Prospect, <br />
            <span className="font-light">With Your Eyes Closed.</span>
          </h1>

          <p className="text-xl text-[#7a7a7a] mb-12 w-full text-left font-light">
            s-esther is the{" "}
            <span className="font-medium">prospecting agent</span> that
            evaluates your lead&apos;s intent completely autonomously giving a {" "}
              <Tooltip>
                <TooltipTrigger asChild>
                  <span className="font-medium cursor-pointer underline decoration-dotted">
                    62.5% reduction
                  </span>
                </TooltipTrigger>
                <TooltipContent className="bg-white text-gray-900 border border-gray-300 p-0 border-0 bg-transparent">
                  <motion.div
                    initial={{ opacity: 0, y: 10, scale: 0.95 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    exit={{ opacity: 0, y: 10, scale: 0.95 }}
                    transition={{ duration: 0.2, ease: "easeOut" }}
                    className="bg-white text-gray-900 border border-gray-300 rounded-md px-3 py-1.5 text-xs shadow-lg"
                  >
                    <p>From 4 minutes → 1.5 minutes!</p>
                  </motion.div>
                </TooltipContent>
              </Tooltip>{" "}
            in research and intent validation.
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
                className="w-full h-16 font-light !text-lg bg-white border-1 border-[#868686] rounded-sm mt-0 pl-12 pr-20"
              />
            </div>
          </div>
          <div className="w-full flex flex-col mb-8">
            <div className="p-2 flex flex-row justify-center items-center gap-2 max-w-[230px] bg-[#FFEFE8] border-2 border-b-0 border-dotted border-[#888888] rounded-sm font-light">
              
              WHAT&apos;S YOUR INTENT?
              <img src="/target_icon.png" alt="cursor" className="w-4 h-4" />
            </div>
            <div className="relative w-full">
            <Textarea
              value={intentValue}
              onInput={handleIntentChange}
              placeholder="Evaluate whether their company would like to buy a developer tool that does automated PR reviews targetted towards engineering heavy organizations..."
              className="w-full h-48 font-light !text-lg bg-white border-1 border-[#868686] focus:border-[#868686] focus:ring-0 focus-visible:border-[#868686] focus-visible:ring-0 focus-visible:ring-offset-0 rounded-sm mt-0 p-4 justify-start items-start align-top"
            />
            </div>
            <div className="w-full flex justify-end mt-2">
              <Button
                onClick={handleSearch}
                size="sm"
                className="h-12 px-8 w-32 rounded-[4px]"
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
