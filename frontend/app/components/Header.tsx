"use client";

import { motion } from "framer-motion";
import React from "react";

const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
          <motion.img
            src="/esther_orange.png"
            alt="Esther Orange"
            className="w-10 h-10 mr-4 mt-2 pointer-events-none select-none object-cover "
            style={{ zIndex: 1 }}
            animate={{ rotate: [0, 15, -15, 0] }}
            transition={{
              duration: 6,
              repeat: Infinity,
              repeatType: "reverse",
              ease: "easeInOut",
            }}
          />
            <h1 className="text-2xl font-light text-black">S-ESTHER</h1>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
