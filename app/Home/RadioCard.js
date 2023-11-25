import {
  Box,
  useRadio,
  useRadioGroup,
  HStack,
  ChakraProvider,
} from "@chakra-ui/react";
import { useEffect } from "react";

export default function RadioCard({ setRadioValue }) {
  const options = ["Table", "Map"];

  const { getRootProps, getRadioProps } = useRadioGroup({
    name: "framework",
    defaultValue: "Table",
    onChange: handleRadio,
  });

  const group = getRootProps();

  useEffect(() => {
    if (setRadioValue) {
      setRadioValue("Table");
    }
  }, []);

  function handleRadio(value) {
    setRadioValue(value);
  }

  return (
    <div className="px-4 py-16">
      <ChakraProvider>
        <HStack {...group}>
          {options.map((value) => {
            const radio = getRadioProps({ value });
            const { getInputProps, getCheckboxProps } = useRadio(radio);

            const inputProps = getInputProps();
            const checkboxProps = getCheckboxProps();

            return (
              <div className="mt-8">
                <Box as="label" key={value}>
                  <input {...inputProps} />
                  <Box
                    {...checkboxProps}
                    cursor="pointer"
                    borderWidth="1px"
                    borderRadius="md"
                    boxShadow="md"
                    display="inline-block"
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
                    {value}
                  </Box>
                </Box>
              </div>
            );
          })}
        </HStack>
      </ChakraProvider>
    </div>
  );
}