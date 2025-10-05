"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface LandingViewProps {
  onButtonClick: () => void;
}

const LandingView: React.FC<LandingViewProps> = ({ onButtonClick }) => {
  const [inputValue, setInputValue] = useState("");
  const [open, setOpen] = useState(false);

  const mockApiResponse = {
    profiles: [
      {
        name: "Daniel Caesar",
        profile_link:
          "https://www.linkedin.com/in/daniel-caesar-68b65390?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABNRNQsB2xj0BqfBum4SYz6AvPDF2T-yH70",
        job_title: "Chief Executive Officer at Caribbean Supply Chain limited",
        location: "Barbados",
        profile_image_url:
          "https://media.licdn.com/dms/image/v2/C4D03AQFfdCwOwDKWMA/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1527265350014?e=1762387200&v=beta&t=sGE-J7lOs6hPo7o3sqSdXUdS7shnnu9KeGLAqtlofjc",
        platform: "linkedin",
      },
      {
        name: "Daniel Cäsar",
        profile_link:
          "https://www.linkedin.com/in/daniel-c%C3%A4sar-7460481b5?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADIEjiYBHLhFquAJ9xtOpVKwebjAfLZOgAE",
        job_title:
          "M.Sc. RWTH | Energy Engineer | Infrastructure Development Expert",
        location: "Vienna",
        profile_image_url:
          "https://media.licdn.com/dms/image/v2/D4D03AQH2tSigR3DGZQ/profile-displayphoto-shrink_100_100/B4DZRw3meLHcAg-/0/1737060412458?e=1762387200&v=beta&t=cQXq4wO6khUmzOrmleZdsvapL2fbwrKKqlFiYptmaBA",
        platform: "linkedin",
      },
      {
        name: "Daniel Caesar",
        profile_link:
          "https://www.linkedin.com/in/daniel-caesar-7a9bb599?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABUANTEBhFPqBYwavTJlX4Q-y8EOhyABYuQ",
        job_title: "Software Product Manager at Instron",
        location: "Boston, MA",
        profile_image_url: null,
        platform: "linkedin",
      },
      {
        name: "Danielle Caesar",
        profile_link:
          "https://www.linkedin.com/in/danielle-caesar-b16b0b9b?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABVYBIIBey-BlYECaG72ng9GUJVOP7IIPpo",
        job_title: "The Pop Shop",
        location: "Ajax, ON",
        profile_image_url:
          "https://media.licdn.com/dms/image/v2/C4E03AQFhqipSlyqsBg/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1516993846562?e=1762387200&v=beta&t=Oa9KOh8AFOhPXC5TjeBpGGkUWPCilYyrEEAqsDrRa-0",
        platform: "linkedin",
      },
      {
        name: "Daniel Caesar",
        profile_link:
          "https://www.linkedin.com/in/daniel-caesar-407701180?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACrRnQcBE8CTRv6Jiz3RFDACVLoLyJ3swTQ",
        job_title:
          "SDR Team Lead at Easy Metrics | Driving Efficiency in Warehouse & Distribution Operations",
        location: "Portland, ME",
        profile_image_url:
          "https://media.licdn.com/dms/image/v2/D4D03AQEEnbDGGGiS6w/profile-displayphoto-shrink_100_100/profile-displayphoto-shrink_100_100/0/1705583026653?e=1762387200&v=beta&t=yc1VJTp4crUYnxgAgMgioYkNFuMJjkbF83-rLP21Bcc",
        platform: "linkedin",
      },
    ],
    total_found: 5,
    query: "daniel caesar",
    success: true,
    error_message: null,
  };

  const suggestedUsers = mockApiResponse.profiles;

  const filteredUsers = suggestedUsers.filter(
    (user) =>
      user.name.toLowerCase().includes(inputValue.toLowerCase()) ||
      user.job_title.toLowerCase().includes(inputValue.toLowerCase()) ||
      user.location.toLowerCase().includes(inputValue.toLowerCase())
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
    setOpen(e.target.value.length > 0);
  };

  const handleUserSelect = (user: (typeof suggestedUsers)[0]) => {
    setInputValue(user.name);
    setOpen(false);
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
                placeholder="Type in a person's name..."
                className="w-full h-16 font-light !text-md bg-white border-2 border-[#fff] rounded-sm mt-0 pl-12 pr-20"
              />
              <Button
                onClick={onButtonClick}
                size="sm"
                className="absolute right-2 top-1/2 transform -translate-y-1/2 h-12 px-8 rounded-[4px]"
              >
                Search
              </Button>

              {open && filteredUsers.length > 0 && (
                <div className="absolute top-full left-0 right-0 mt-1 bg-white border-2 border-[#fff] rounded-sm shadow-lg z-20">
                  <div className="max-h-72 overflow-y-auto">
                    {filteredUsers.map((user, index) => (
                      <div
                        key={`${user.name}-${index}`}
                        onClick={() => handleUserSelect(user)}
                        className="flex items-center gap-3 p-3 hover:bg-gray-50 cursor-pointer border-gray-100"
                      >
                        {user.profile_image_url ? (
                          <img
                            src={user.profile_image_url}
                            alt={user.name}
                            className="w-10 h-10 rounded-full object-cover"
                          />
                        ) : (
                          <div className="w-10 h-10 rounded-full bg-gray-300 flex items-center justify-center">
                            <span className="text-gray-600 text-sm font-medium">
                              {user.name
                                .split(" ")
                                .map((n) => n[0])
                                .join("")}
                            </span>
                          </div>
                        )}
                        <div className="flex flex-col items-start">
                          <div className="font-semibold">{user.name}</div>
                          <div className="text-sm text-[#888888]">
                            {user.job_title}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingView;
