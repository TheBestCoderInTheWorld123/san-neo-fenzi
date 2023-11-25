"use client";
import React, { useState } from "react";
import RadioCard from "./RadioCard";
import { Box } from "@chakra-ui/react";

export default function RadioButton() {
  const [radioValue, setRadioValue] = useState("");

  const handleRadioChange = (value) => {
    setRadioValue(value);
  };

  return (

    <Box className="px-4 mt-16">
      <RadioCard setRadioValue={handleRadioChange} />
      <Box
        cursor="pointer"
        borderWidth="1px"
        borderRadius="md"
        boxShadow="md"
        _checked={{
          bg: "teal.600",
          color: "white",
          borderColor: "teal.600",
        }}
        _focus={{
          boxShadow: "outline",
        }}
        px={5}
        py={3}
        marginTop="10px"
        display="inline-block"
      >
        Selected Value: {radioValue}
      </Box>
    </Box>
  );
}