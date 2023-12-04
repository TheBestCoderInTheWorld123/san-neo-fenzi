import {
  Box,
  useRadioGroup,
  useRadio,
  HStack,
  ChakraProvider,
} from "@chakra-ui/react";
import { useEffect } from "react";

function RadioOption({ radio }) {
  const { getInputProps, getCheckboxProps } = useRadio(radio);
  const inputProps = getInputProps();
  const checkboxProps = getCheckboxProps();

  return (
    <Box className="m-4" as="label">
      <input {...inputProps} />
      <Box className="cursor-pointer border-spacing-4 display:inline-block border-black shadow-md border-1 rounded-md"
        {...checkboxProps}
        _checked={{
          bg: "#2f455c",
          color: "white",
          borderColor: "#2f455c",
        }}
        _focus={{
          boxShadow: "outline",
        }}
        px={5}
        py={3}
      >
        {radio.value}
      </Box>
    </Box>
  );
}

export default function RadioCard({ setRadioValue }) {
  const options = ["Table", "Map"];
  const { getRootProps, getRadioProps } = useRadioGroup({
    name: "framework",
    defaultValue: "Table",
    onChange: (value) => {
      console.log("RadioCard onChange called with:", value); // Add this for debugging
      setRadioValue(value);
    },
  });

  const group = getRootProps();

  useEffect(() => {
    setRadioValue("Table");
  }, []);

  return (
    <ChakraProvider>
      <HStack {...group}>
        {options.map((value) => {
          const radio = getRadioProps({ value });
          return <RadioOption key={value} radio={radio} />;
        })}
      </HStack>
    </ChakraProvider>
  );
}
