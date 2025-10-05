"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import LandingView from "./views/LandingView";
import LoadingView from "./views/LoadingView";
import ResultView from "./views/ResultView";
import DottedGrid from "./components/DottedGrid";

type SSEStep = {
  message: string;
  completed: boolean;
};

export default function Home() {
  const [currentPage, setCurrentPage] = useState<
    "landing" | "loading" | "result"
  >("landing");
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [steps, setSteps] = useState<SSEStep[]>([]);
  const [currentStepMessage, setCurrentStepMessage] = useState("");
  const [prospectingResult, setProspectingResult] = useState<any>(null);

  const handleLandingButtonClick = async (url: string) => {
    setLinkedinUrl(url);
    setCurrentPage("loading");
    setSteps([]);
    setCurrentStepMessage("");
    setProspectingResult(null);

    try {
      const response = await fetch("http://localhost:8000/core/v1/start_prospecting", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          profile_url: url,
          intent: "does this person have intent of buying a dev tool",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error("Response body is null");
      }

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const jsonData = JSON.parse(line.substring(6));

              if (jsonData.type === "tool_started") {
                const message = `${jsonData.tool_name}`;
                setCurrentStepMessage(message);
              } else if (jsonData.type === "tool_completed") {
                setSteps(prev => [...prev, { message: currentStepMessage || jsonData.tool_name, completed: true }]);
                setCurrentStepMessage("");
              } else if (jsonData.type === "final_result") {
                setProspectingResult(jsonData.summary);
                setTimeout(() => {
                  setCurrentPage("result");
                }, 1000);
              } else if (jsonData.type === "error") {
                console.error("Error from API:", jsonData.message);
                setSteps(prev => [...prev, { message: `Error: ${jsonData.message}`, completed: true }]);
              }
            } catch (e) {
              console.error("Failed to parse JSON:", e);
            }
          }
        }
      }
    } catch (error) {
      console.error("Failed to connect to API:", error);
      setSteps(prev => [...prev, { message: "Failed to connect to backend", completed: true }]);
    }
  };

  const handleRestart = () => {
    setCurrentPage("landing");
    setLinkedinUrl("");
    setSteps([]);
    setCurrentStepMessage("");
    setProspectingResult(null);
  };

  const getTranslateX = () => {
    switch (currentPage) {
      case "landing":
        return "0";
      case "loading":
        return "-100vw";
      case "result":
        return "-200vw";
      default:
        return "0";
    }
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      {/* Container for everything that slides horizontally */}
      <motion.div
        className="relative flex w-[300vw] h-full"
        animate={{ x: getTranslateX() }}
        transition={{
          duration: 1,
          ease: [0.25, 0.1, 0.25, 1],
          type: "tween",
        }}
      >
        {/* Grid background that spans all views */}
        <div className="absolute inset-0 w-full h-full">
          <DottedGrid />
        </div>

        {/* Content container */}
        <div className="relative z-10 flex w-full h-full">
          {/* Landing page view */}
          <div className="w-screen h-full">
            <LandingView onButtonClick={handleLandingButtonClick} />
          </div>

          {/* Loading page view */}
          <div className="w-screen h-full">
            <LoadingView steps={steps} currentStepMessage={currentStepMessage} />
          </div>

          {/* Result page view */}
          <div className="w-screen h-full">
            <ResultView onRestart={handleRestart} result={prospectingResult} />
          </div>
        </div>
      </motion.div>
    </div>
  );
}
