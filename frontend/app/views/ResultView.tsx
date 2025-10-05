"use client";

import React, { useEffect } from "react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { Button } from "@/components/ui/button";

interface ResultViewProps {
  onRestart?: () => void;
  result?: any;
}

const ResultView: React.FC<ResultViewProps> = ({ onRestart, result }) => {
  const scoreData = {
    value: 79,
    label: "Score",
  };

  // Animation setup
  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest));

  useEffect(() => {
    const controls = animate(count, scoreData.value, {
      duration: 2,
      ease: "easeOut",
    });
    return controls.stop;
  }, [count, scoreData.value]);

  const analysisData = {
    good: [
      "Posted on LinkedIn about the exact problem your tool solves",
      "Tech stack matches your integrations",
      "Uses a competitor product",
    ],
    bad: [
      "Company inactive or under 5 employees",
      "Clicked but never came back",
    ],
  };

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
        <motion.img
          src="/esther_blue.png"
          alt="Esther Blue"
          className="absolute bottom-14 right-14 w-80 h-80 pointer-events-none select-none object-cover"
          style={{ zIndex: 1 }}
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{
            duration: 8,
            repeat: Infinity,
            repeatType: "reverse",
            ease: "easeInOut",
          }}
        />
        
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#ECFFD2]/40 rounded-md p-8 border-1 border-[#868686]">
          <h1 className="text-6xl text-gray-900 mb-6 w-full text-left font-light">
            <span className="font-semibold">Marc,</span>
            <br /> At A Glance
          </h1>
          <p className="text-xl text-[#7a7a7a] mb-12 w-full text-left font-light">
            Prospecting scores are guides, not guarantees. They help you
            prioritize, but don't assume a high score means they'll buy.
          </p>

          {result && (
            <div className="w-full mb-6 p-4 bg-white rounded-lg">
              <p className="text-sm text-gray-600 font-mono whitespace-pre-wrap break-words">
                {JSON.stringify(result, null, 2)}
              </p>
            </div>
          )}
          <div className="flex w-full flex-col items-start justify-start">
            <h2 className="text-lg font-semibold text-gray-800 mb-1">
              {scoreData.label}
            </h2>
            <motion.h2 className="text-5xl font-semibold text-gray-800 mb-4">
              {rounded}
            </motion.h2>
          </div>

          <div className="w-full mb-8">
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-left">The good</h3>
              <ul className="space-y-2 text-left">
                {analysisData.good.map((item, index) => (
                  <li key={index} className="text-gray-700">
                    • {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-left">The bad</h3>
              <ul className="space-y-2 text-left">
                {analysisData.bad.map((item, index) => (
                  <li key={index} className="text-gray-700">
                    • {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="flex w-full flex-col items-start justify-start">
            {onRestart && (
              <Button
                onClick={onRestart}
                size="sm"
                className="h-12 px-8 rounded-[4px]"
              >
                Start Over
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultView;
