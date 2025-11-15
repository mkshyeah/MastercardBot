import React, { useState } from "react";
import { QueryInput } from "./QueryInput";

const Spinner = () => (
  <svg className="animate-spin h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
  </svg>
);

const TableView = ({ data }) => {
  if (!data || !Array.isArray(data) || data.length === 0) return null;
  const headers = Object.keys(data[0]);
  return (
    <div className="border-t pt-3 mt-3">
      <h3 className="font-semibold mb-2 text-sm">Табличные данные</h3>
      <div className="overflow-x-auto rounded-lg border">
        <table className="min-w-full divide-y-2 divide-gray-200 bg-white text-sm">
          <thead className="text-left">
            <tr>
              {headers.map((header) => (<th key={header} className="whitespace-nowrap px-4 py-2 font-medium text-gray-900">{header}</th>))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {data.map((row, rowIndex) => (<tr key={rowIndex}>{headers.map((header) => (<td key={`${rowIndex}-${header}`} className="whitespace-nowrap px-4 py-2 text-gray-700">{String(row[header])}</td>))}</tr>))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const ResultsView = () => {
  const [backendResponse, setBackendResponse] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async (text) => {
    try {
      setError(null);
      setLoading(true);
      setBackendResponse(null);
      const body = { user_query: text };
      const resp = await fetch("http://127.0.0.1:8000/query", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      if (!resp.ok) {
        const textData = await resp.text();
        throw new Error(`Ошибка запроса: ${resp.status} ${textData}`);
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
    <div className="min-h-screen w-full flex justify-center bg-linear-to-br from-[#f8f5ed] to-[#e6ddd0] px-4 py-10 lg:py-20">
      <div className="w-full max-w-6xl flex flex-col lg:flex-row items-center lg:items-start gap-10">
        
        {/* Левая колонка с заголовком и вводом */}
        <div className="flex-1 flex flex-col justify-center gap-6 items-center lg:items-start">
          <div>
            <h1 className="text-3xl lg:text-4xl font-semibold mb-3 text-center lg:text-left">
              Real-Time Financial Analytics.
            </h1>
            <p className="text-sm lg:text-base text-stone-600 max-w-md text-center lg:text-left">
              Введите запрос на естественном языке, а мы превратим его в
              <strong> SQL-запрос</strong> и вернём вам готовый ответ.
            </p>
          </div>
          <div className="w-full">
            <QueryInput
              name="request"
              id="request"
              inputText=""
              btnText={loading ? "Загружаю..." : "Отправить"}
              onRun={handleRun}
            />
          </div>
        </div>

        {/* Правая колонка с результатами */}
        <div className="flex-1 flex justify-center lg:justify-end w-full">
          <div className="w-full max-w-[520px] rounded-3xl bg-[#dde7f5] px-6 py-8 flex flex-col items-center gap-4">
            {!backendResponse && !error && !loading && (
              <div className="w-full bg-white rounded-xl shadow p-4"><pre className="text-xs whitespace-pre-wrap text-gray-400">Ждем запрос...</pre></div>
            )}
            {loading && (
              <div className="w-full flex justify-center items-center bg-white rounded-xl shadow p-4"><Spinner /><p className="text-sm text-gray-500 ml-3">Обработка запроса...</p></div>
            )}
            {error && (<div className="w-full bg-red-100 text-red-800 rounded-xl shadow p-4 text-sm">{error}</div>)}
            {backendResponse && (
              <div className="w-full bg-white rounded-xl shadow p-4 flex flex-col gap-3 animate-fade-in">
                <div>
                  <h2 className="font-semibold mb-1">Ответ</h2>
                  <p className="text-sm">{backendResponse.summary}</p>
                </div>
                <TableView data={backendResponse.result} />
                <SqlDebug sql={backendResponse.sql_query} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsView;

const SqlDebug = ({ sql }) => {
  const [open, setOpen] = useState(false);
  if (!sql) return null;
  return (
    <div className="border-t pt-3 mt-3">
      <button className="text-xs text-stone-500 underline" onClick={() => setOpen((o) => !o)}>
        {open ? "Скрыть технические детали" : "Показать технические детали"}
      </button>
      {open && (<pre className="text-xs whitespace-pre-wrap bg-stone-100 p-2 rounded mt-1">{sql}</pre>)}
    </div>
  );
};
