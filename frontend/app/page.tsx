"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import LandingView from "./views/LandingView";
import LoadingView from "./views/LoadingView";
import ResultView from "./views/ResultView";
import DottedGrid from "./components/DottedGrid";

export default function Home() {
  const [currentPage, setCurrentPage] = useState<
    "landing" | "loading" | "result"
  >("landing");

  const handleLandingButtonClick = () => {
    setCurrentPage("loading");
  };

  const handleRestart = () => {
    setCurrentPage("landing");
  };

  useEffect(() => {
    if (currentPage === "loading") {
      const timer = setTimeout(() => {
        setCurrentPage("result");
      }, 9000);
      return () => clearTimeout(timer);
    }
  }, [currentPage]);

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
            <LoadingView />
          </div>

          {/* Result page view */}
          <div className="w-screen h-full">
            <ResultView onRestart={handleRestart} />
          </div>
        </div>
      </motion.div>
    </div>
  );
}
