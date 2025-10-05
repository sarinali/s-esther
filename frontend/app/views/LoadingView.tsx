"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { TextShimmer } from "@/components/motion-primitives/text-shimmer";

interface LoadingViewProps {
  onComplete?: () => void;
}

const LoadingView: React.FC<LoadingViewProps> = ({ onComplete }) => {
  const [currentStep, setCurrentStep] = useState(0) ;

  const steps = [
    "Got LinkedIn Portfolio",
    "Analyzing User's Likes",
    "Evaluating User's Comments",
    "Investigating User's Postssss",
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < steps.length - 1) {
          return prev + 1;
        } else {
          clearInterval(interval);
          setTimeout(() => {
            onComplete?.();
          }, 3000);
          return prev;
        }
      });
    }, 3000);

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div className="relative z-10 flex items-center justify-center h-full">
        <div className="w-[800px] h-[800px] flex flex-col items-center justify-start text-center bg-[#E8E6FF] rounded-lg p-8">
          <h1 className="text-6xl text-gray-900 mb-6 w-full text-left font-light">
            Watch The <span className="font-semibold">Magic</span> Unfold
          </h1>

          <div className="flex flex-col gap-4 w-full mt-8">
            {steps.map((step, index) => (
              <div key={step} className="flex items-center gap-4">
                <div className="w-6 h-6 flex items-center justify-center">
                  {index < currentStep ? (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ duration: 0.3 }}
                      className="w-5 h-5 bg-green-500 rounded-full flex items-center justify-center"
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
                  ) : index === currentStep ? (
                    <></>
                  ) : (
                    <div className="w-6 h-6 border-2 border-gray-200 rounded-full" />
                  )}
                </div>
                {index === currentStep ? (
                  <TextShimmer
                    as="span"
                    className="text-lg "
                    duration={1.5}
                  >
                    {step}
                  </TextShimmer>
                ) : index < currentStep ? (
                  <span className="text-lg text-gray-900">
                    {step}
                  </span>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoadingView;
