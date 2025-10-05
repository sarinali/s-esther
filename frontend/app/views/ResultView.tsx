"use client";

import React, { useEffect } from "react";
import { motion, useMotionValue, useTransform, animate } from "framer-motion";
import { Button } from "@/components/ui/button";

interface ResultViewProps {
  onRestart?: () => void;
  result?: any;
  linkedinUrl?: string;
}

const ResultView: React.FC<ResultViewProps> = ({ onRestart, result, linkedinUrl }) => {
  const extractNameFromUrl = (url: string): string => {
    if (!url) return "Marc";
    const match = url.match(/\/in\/([^\/]+)/);
    if (match) {
      const slug = match[1];
      const name = slug.split('-').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
      ).join(' ');
      return name.split(' ')[0];
    }
    return "Marc";
  };

  const firstName = extractNameFromUrl(linkedinUrl || "");
  const scoreValue = result?.score ?? 79;
  const goodSignals = result?.good_signals ?? [
    "No relevant good signals",
  ];
  const badSignals = result?.bad_signals ?? [
    "No relevant bad signals",
  ];
  const reasoning = result?.reasoning ?? "";

  const count = useMotionValue(0);
  const rounded = useTransform(count, (latest) => Math.round(latest));

  useEffect(() => {
    const controls = animate(count, scoreValue, {
      duration: 2,
      ease: "easeOut",
    });
    return controls.stop;
  }, [count, scoreValue]);

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
       
        
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#ECFFD2] rounded-lg p-8 overflow-y-auto relative">
          <h1 className="text-6xl text-gray-900 mb-6 w-full text-left font-light">
            <span className="font-semibold">{firstName},</span>
            <br /> At A Glance
          </h1>
          <p className="text-xl text-[#7a7a7a] mb-12 w-full text-left font-light">
            Prospecting scores are guides, not guarantees. They help you
            prioritize, but don't assume a high score means they'll buy.
          </p>

          <div className="flex w-full flex-col items-start justify-start">
            <h2 className="text-lg font-semibold text-gray-800 mb-1">
              Score
            </h2>
            <motion.h2 className="text-5xl font-semibold text-gray-800 mb-4">
              {rounded}
            </motion.h2>
          </div>

          {reasoning && (
            <div className="w-full mb-6">
              <h3 className="text-lg font-semibold mb-3 text-left">Reasoning</h3>
              <p className="text-gray-700 text-left">{reasoning}</p>
            </div>
          )}

          <div className="w-full mb-8">
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-left">The good</h3>
              <ul className="space-y-2 text-left">
                {goodSignals.map((item: string, index: number) => (
                  <li key={index} className="text-gray-700">
                    • {item}
                  </li>
                ))}
              </ul>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-left">The bad</h3>
              <ul className="space-y-2 text-left">
                {badSignals.map((item: string, index: number) => (
                  <li key={index} className="text-gray-700">
                    • {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {onRestart && (
            <Button
              onClick={onRestart}
              size="sm"
              className="h-12 px-8 rounded-[4px] sticky bottom-2 left-full "
            >
              Start Over
            </Button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultView;
