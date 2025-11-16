import React, { useState } from "react";

const CARD_CONFIG = {
  standard: {
    title: "standard",
    bg: "#c28a55",
    textColor: "#ffffff",
  },
  world: {
    title: "world",
    bg: "#153852",
    textColor: "#ffffff",
  },
  platinum: {
    title: "platinum",
    bg: "#b3b5ba",
    textColor: "#ffffff",
  },
  elite: {
    title: "world elite",
    bg: "#18191b",
    textColor: "#ffffff",
  },
};

export const QueryInput = ({ name, id, inputText, btnText, onRun }) => {
  const [value, setValue] = useState(inputText || "");

  const [cardType, setCardType] = useState("standard");

  const currentCard = CARD_CONFIG[cardType] ?? CARD_CONFIG.standard;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!value.trim()) return;
    onRun(value.trim());
  };

  return (
<<<<<<< HEAD
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 w-full max-w-md">
=======
    <form
      onSubmit={handleSubmit}
      className="flex flex-col gap-3 w-full max-w-md"
    >
>>>>>>> 2dc8d2b (feat: Обновил UI и почистил комментарии в бэке)
      {/* выбор типа / цвета карты */}
      <select
        value={cardType}
        onChange={(e) => setCardType(e.target.value)}
        className="mb-2 w-40 rounded-lg bg-[#fff6db] px-3 py-2 text-sm shadow-xs"
      >
        <option value="standard">Standard</option>
        <option value="elite">World Elite</option>
        <option value="world">World</option>
        <option value="platinum">Platinum</option>
      </select>

      {/* карточка — только фон и цвет текста  */}
      <div
        className="rounded-3xl p-6 shadow-xl transition-colors duration-300 relative"
        style={{
          backgroundColor: currentCard.bg,
          color: currentCard.textColor,
        }}
      >
        <div className="flex items-center justify-between mb-4">
          <div className="text-lg font-medium">{currentCard.title}</div>
<<<<<<< HEAD
          <div className="flex items-center gap-1">
            <span className="w-10 h-10 rounded-full bg-[#eb001b]" />
            <span className="w-10 h-10 rounded-full bg-[#f79e1b] -ml-3 opacity-90" />
          </div>
        </div>

        {/* поле ввода */}
        <div className="bg-[#fff6db] rounded-2xl p-3 mb-4">
          <textarea
            id={id}
            name={name}
            className="w-full bg-transparent outline-none resize-none text-sm text-black"
            placeholder="Введите запрос..."
            rows={4}
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
        </div>

        <button
          type="submit"
          className="px-6 py-2 rounded-lg bg-[#b57a45] text-white text-sm font-medium"
        >
          {btnText}
        </button>
=======
        </div>

        {/* поле ввода */}
        <div className="bg-[#fff6db] rounded-2xl p-3 mb-4">
          <textarea
            id={id}
            name={name}
            className="w-full bg-transparent outline-none resize-none text-sm text-black"
            placeholder="Введите запрос..."
            rows={4}
            value={value}
            onChange={(e) => setValue(e.target.value)}
          />
        </div>

        <div className="flex justify-between">
          <button
            type="submit"
            className="px-6 py-2 rounded-lg bg-[#b57a45] text-white text-sm font-medium"
          >
            {btnText}
          </button>
          <div className="flex flex-col gap-2 items-center">
            <div className="flex items-center gap-1">
              <span className="w-10 h-10 rounded-full bg-[#eb001b] border border-red-600 -mr-3 opacity-80" />
              <span className="w-10 h-10 rounded-full bg-[#f79e1b] " />
            </div>
            <span>mastercard</span>
          </div>
        </div>
>>>>>>> 2dc8d2b (feat: Обновил UI и почистил комментарии в бэке)
      </div>
    </form>
  );
};