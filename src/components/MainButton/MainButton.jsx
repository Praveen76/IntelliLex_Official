import { useEffect, useRef } from "react";
import ReactDOM from "react-dom";

export function MainButton({ input, onClick }) {
  const buttonRef = useRef(null);

  useEffect(() => {
    const button = buttonRef.current;
    if (!button) return;

    const wrapper = document.createElement("span");
    wrapper.style.display = "inline-block";
    wrapper.style.marginLeft = "5px";
    wrapper.appendChild(button);

    const parent = input.parentNode;
    parent.insertBefore(wrapper, input.nextSibling);

    return () => {
      if (wrapper.parentNode) {
        wrapper.parentNode.removeChild(wrapper);
      }
    };
  }, [input]);

  return ReactDOM.createPortal(
    <button
      ref={buttonRef}
      onClick={onClick}
      className="px-2 py-1 bg-green-500 text-white rounded- hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
    >
      ✨
    </button>,
    document.body
  );
}
