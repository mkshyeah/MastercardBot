import React, { useState } from "react";
import { QueryInput } from "./QueryInput";

const ResultsView = () => {
  const [parsed, setParsed] = useState(null);
  const [backendResponse, setBackendResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const [language, setLanguage] = useState("ru");

  const handleRun = async (text) => {
    try {
      setError(null);
      setLoading(true);
      setBackendResponse(null);

      const body = { user_query: text };

      setParsed(body);

      const resp = await fetch("http://127.0.0.1:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      if (!resp.ok) {
        const text = await resp.text();
        throw new Error(`Ошибка запроса: ${resp.status} ${text}`);
      }

      const data = await resp.json();
      setBackendResponse(data);
    } catch (e) {
      console.error(e);
      setError(e.message || "Что-то пошло не так");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen w-full
    flex flex-col items-center justify-start
    bg-linear-to-br from-[#f8f5ed] to-[#e6ddd0]
    p-4 gap-4
    lg:p-1 lg:gap-1
    lg:flex-row lg:items-start"
    >
      <div className="flex flex-1 justify-center">
        <QueryInput
          name="request"
          id="request"
          inputText=""
          btnText={loading ? "Загружаю..." : "Отправить"}
          onRun={handleRun}
          language={language}
          onLanguageChange={setLanguage}
        />
      </div>
      <div className="flex flex-1 justify-center">
        {/* Блок для JSON */}
        <div className="flex flex-col gap-4">
          <div className="w-[400px] bg-white rounded-xl shadow p-4">
            <h2 className="font-semibold mb-2">
              JSON, который уходит на /query
            </h2>
            <pre className="text-xs whitespace-pre-wrap">
              {parsed
                ? JSON.stringify(parsed, null, 2)
                : "Ещё ничего не отправляли"}
            </pre>
          </div>

          {/* Проверка на ошибки */}
          {error && (
            <div className="w-[400px] bg-red-100 text-red-800 rounded-xl shadow p-4 text-sm">
              {error}
            </div>
          )}
        </div>
        {backendResponse && (
          <div className="w-[400px] bg-white rounded-xl shadow p-4 flex flex-col gap-3">
            <div>
              <h2 className="font-semibold mb-1">Ответ</h2>
              <p className="text-sm">{backendResponse.summary}</p>
            </div>

            <SqlDebug sql={backendResponse.sql_query} />
          </div>
        )}
      </div>
    </div>
  );
};
export default ResultsView;

const SqlDebug = ({ sql }) => {
  const [open, setOpen] = useState(false);
  if (!sql) return null;

  return (
    <div className="border-t pt-2 mt-2">
      <button
        className="text-xs text-stone-500 underline"
        onClick={() => setOpen((o) => !o)}
      >
        {open ? "Скрыть технические детали" : "Показать технические детали"}
      </button>
      {open && (
        <pre className="text-xs whitespace-pre-wrap bg-stone-100 p-2 rounded mt-1">
          {sql}
        </pre>
      )}
    </div>
  );
};
