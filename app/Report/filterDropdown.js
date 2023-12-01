import React, { useState } from "react";
import Select from "react-select";

const FilterDropdown = ({ selectedColumn, onChange }) => {
  const [selectValue, setSelectValue] = useState(selectedColumn);
  const [showInput, setShowInput] = useState(false);

  const handleSelectChange = (event) => {
    const selectedValue = event.value;
    setSelectValue(selectedValue);
    onChange(selectedValue);

    if (selectedValue) {
      setShowInput(true);
    } else {
      setShowInput(false);
    }
  };

  const options = [
    { value: "device_serial_number", label: "Sr. No." },
    { value: "latest_recorded_date", label: "Timestamp" },
    { value: "tags.AQ", label: "AQ" },
    { value: "tags.HUM", label: "HUM" },
    { value: "tags.TMP", label: "TMP" },
  ];

  return (
    <div className="flex mr-6">
      <label className="mx-2">Filter By:</label>
      <Select
        value={selectValue}
        onChange={handleSelectChange}
        options={options}
      />
      {showInput && (
        <input
          type="text"
          id="filterInput"
          onKeyUp={(event) => {
            console.log(`Filter text: ${event.target.value}`);
          }}
        />
      )}
    </div>
  );
};

export default FilterDropdown;
