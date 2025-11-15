import React, { useState } from "react";

export const LanguageSwitcher = ({
  language,
  onChange,
  selectName,
  selectId,
}) => {
  const languages = [
    { value: "ru", label: "RU" },
    { value: "en", label: "EN" },
    { value: "kz", label: "KZ" },
  ];

  return (
    <select
      name={selectName}
      id={selectId}
      className="bg-[#B8936D] w-auto p-1 custom-select rounded-[5px] font-medium"
      value={language}
      onChange={(e) => onChange && onChange(e.target.value)}
    >
      {languages.map((lang) => (
        <option key={lang.value} value={lang.value}>
          {lang.label}
        </option>
      ))}
    </select>
  );
};

export const QueryInput = (props) => {
  const {
    name,
    id,
    inputText = "",
    btnText = "",
    onRun,
    language = "ru",
    onLanguageChange,
  } = props;

  const [value, setValue] = useState(inputText);

  const handleClick = () => {
    if (onRun) {
      onRun(value);
    }
  };
  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-col justify-between items-start w-[400px] h-[250px] bg-[#B8936D] rounded-xl gap-3 shadow-xl p-5">
        <div className="flex flex-col w-full items-end justify-end">
          <div className="relative flex items-center justify-end w-full">
            <div className="w-12 h-12 bg-[#FF4B3E] opacity-90 border border-red-500 rounded-full absolute -translate-x-8"></div>
            <div className="w-12 h-12 bg-[#FFB347] rounded-full"></div>
          </div>
          <span>mastercard</span>
        </div>
        <textarea
          name={name}
          id={id}
          className="w-full h-full bg-amber-50 p-2 rounded-2xl"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Введите запрос..."
        />
      </div>
      <div className="flex w-full justify-between">
        <LanguageSwitcher
          language={language}
          onChange={onLanguageChange}
          selectName="language"
          selectId="language"
        />
        <button
          className="px-5 py-2 bg-[#B8936D] w-[150px] rounded-[5px]"
          onClick={handleClick}
        >
          {btnText}
        </button>
      </div>
    </div>
  );
};
