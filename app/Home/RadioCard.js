import {
  Box,
  useRadioGroup,
  useRadio,
  Switch,
  FormLabel,
  HStack,
  VStack,
  ChakraProvider,
  Spacer,
  Flex
} from "@chakra-ui/react";
import { useEffect, useState } from "react";

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
  const [isMapSelected, setIsMapSelected] = useState(false);
  
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

  const handleToggle = () => {
    setIsMapSelected(!isMapSelected);
    setRadioValue(isMapSelected ? "Table" : "Map");
  };


  return (
    <ChakraProvider>
    <Flex justifyContent="flex-start" alignItems="center">
      <Box>
        <Flex alignItems="center">
          <FormLabel htmlFor="toggle" mb="0" mr={2}> {/* Add a margin to the right of the label */}
            {isMapSelected ? "Map" : "Table"}
          </FormLabel>
          <Switch
            id="toggle"
            isChecked={isMapSelected}
            onChange={handleToggle}
            colorScheme="teal"
            size="md"
          />
        </Flex>
      </Box>
    </Flex>
  </ChakraProvider>
  
  );
}
