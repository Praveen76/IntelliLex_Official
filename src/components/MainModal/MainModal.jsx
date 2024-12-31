import { useEffect, useRef, useState } from "react";

export function MainModal({
  isOpen,
  onClose,
  content,
  buttonPosition,
  inputDiv,
}) {
  const modalRef = useRef(null);
  const [recommendedSentences, setRecommended] = useState([]);
  const [isLoading, setLoading] = useState(false);

  useEffect(() => {
    setRecommended([]);
  }, [isOpen]);

  useEffect(() => {
    console.log(buttonPosition);
    if (isOpen && buttonPosition) {
      const modal = modalRef.current;
      if (modal) {
        modal.style.bottom = `${buttonPosition.bottom - 1600}px`;
        modal.style.right = `${buttonPosition.right + 100}px`;
      }
    }
  }, [isOpen, buttonPosition]);

  const onGenerate = () => {
    if (content == "") {
      return;
    }
    setLoading(true);
    setRecommended([]);
    fetch("http://127.0.0.1:5000/proxy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: content,
      }),
    })
      .then((response) => response.json())
      .then((payload) => {
        setRecommended(payload.responses);
        setLoading(false);
      })
      .catch((errors) => {
        alert(
          "There is a problem requesting recommendation from the server. Try again later!"
        );
        console.error(errors);
        setLoading(false);
      });
  };

  if (!isOpen) return null;

  return (
    <div
      ref={modalRef}
      className="fixed bg-white p-4 rounded-lg shadow-xl max-w-md w-full z-50 border border-gray-200"
      style={{ maxWidth: "300px" }}
    >
      <h2 className="text-lg font-bold mb-2">IntelliLex</h2>
      <p className="mb-4 text-sm">{content}</p>
      <div>
        {recommendedSentences.map((sentence, i) => {
          return (
            <button
              key={"recommended_" + i}
              onClick={onClose}
              className="px-2 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 mb-2"
            >
              {sentence}
            </button>
          );
        })}
      </div>
      <button
        onClick={onClose}
        className="float-right px-2 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50"
      >
        Close
      </button>
      <button
        onClick={onGenerate}
        disabled={isLoading}
        className="float-right px-2 py-1 text-sm bg-green-500 text-white rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
      >
        {isLoading ? "Loading" : "Generate"}
      </button>
    </div>
  );
}
