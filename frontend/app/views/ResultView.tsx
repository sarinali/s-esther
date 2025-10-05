"use client";

import React from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import CountUp from "@/components/CountUp";

interface ResultViewProps {
  onRestart?: () => void;
  result?: any;
  linkedinUrl?: string;
}

const ResultView: React.FC<ResultViewProps> = ({ onRestart, result, linkedinUrl }) => {
  const firstName = result?.prospect_name?.split(' ')[0] ?? "Marc";
  const scoreValue: number = typeof result?.score === 'number' ? result.score : 79;
  const goodSignals = result?.good_signals ?? [
    "No relevant good signals",
  ];
  const badSignals = result?.bad_signals ?? [
    "No relevant bad signals",
  ];
  const reasoning = result?.reasoning ?? "";

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
       
        
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#ECFFD2]/40 rounded-md p-8 overflow-y-auto relative border-1 border-[#868686]">
          <h1 className="text-6xl text-gray-900 mb-6 w-full text-left font-light">
            <span className="font-semibold">{firstName},</span>
            <br /> At A Glance.
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
              <CountUp to={scoreValue} />
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
