"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { TextShimmer } from "@/components/motion-primitives/text-shimmer";

type SSEStep = {
  title: string;
  description: string;
  completed: boolean;
};

interface LoadingViewProps {
  steps: SSEStep[];
  currentStep: {
    title: string;
    description: string;
  } | null;
}

const LoadingView: React.FC<LoadingViewProps> = ({ steps, currentStep }) => {

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#E8E6FF] rounded-lg p-8">
          <h1 className="text-6xl text-gray-900 mb-6 w-full text-left font-light">
            Watch The <span className="font-semibold">Magic</span> Unfold
          </h1>

          <div className="flex flex-col gap-4 w-full mt-8">
            {steps.map((step, index) => (
              <div key={index} className="flex items-start gap-4">
                <div className="w-6 h-6 flex items-center justify-center mt-1">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.3 }}
                    className="w-5 h-5 bg-black rounded-full flex items-center justify-center"
                  >
                    <svg
                      className="w-4 h-4 text-white"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </motion.div>
                </div>
                <div className="flex flex-col items-start">
                  <span className="text-lg font-semibold text-gray-900">{step.title}</span>
                  <span className="text-sm text-gray-600">{step.description}</span>
                </div>
              </div>
            ))}
            {currentStep && (
              <div className="flex items-start gap-4">
                <div className="w-6 h-6 flex items-center justify-center mt-1" />
                <div className="flex flex-col items-start">
                  <TextShimmer as="span" className="text-lg font-semibold" duration={1.5}>
                    {currentStep.title}
                  </TextShimmer>
                  <span className="text-sm text-gray-600">{currentStep.description}</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingView;
