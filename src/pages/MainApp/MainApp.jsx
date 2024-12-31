import { useState, useEffect } from "react";
import { MainButton } from "../../components/MainButton/MainButton";
import { MainModal } from "../../components/MainModal/MainModal";

export function MainApp() {
  const [inputs, setInputs] = useState([]);
  const [modalContent, setModalContent] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [buttonPosition, setButtonPosition] = useState(null);
  const [inputDiv, setInputDiv] = useState(null);

  useEffect(() => {
    const findInputs = () => {
      const textInputs = document.querySelectorAll(
        'input[type="text"], textarea'
      );
      const editableElements = document.querySelectorAll("[contenteditable]");
      setInputs([...textInputs, ...editableElements]);
    };

    findInputs();

    const observer = new MutationObserver(findInputs);
    observer.observe(document.body, { childList: true, subtree: true });

    return () => observer.disconnect();
  }, []);

  const handleButtonClick = (input, event) => {
    event.preventDefault();
    const buttonRect = event.target.getBoundingClientRect();
    setButtonPosition({
      top: buttonRect.top + window.scrollY,
      left: buttonRect.left + window.scrollX,
      bottom: buttonRect.bottom + window.scrollY,
      right: buttonRect.right + window.scrollX,
      height: buttonRect.height,
    });
    setModalContent(input.value || input.textContent);
    setInputDiv(input);

    // alert(input.value || input.textContent);
    console.log(input);
    console.log(input.value || input.textContent);
    console.log(document.activeElement);
    // const lexicalEditor = document.querySelector("editor-selector");
    // console.log(lexicalEditor);
    // const inputEvent = new InputEvent("input", {
    //   data: "Your text here hello sir",
    //   inputType: "insertText",
    //   dataTransfer: null,
    //   isComposing: false,
    //   bubbles: true,
    // });
    // lexicalEditor.dispatchEvent(inputEvent);

    setIsModalOpen(true);
  };

  return (
    <>
      {inputs.map((input, index) => (
        <MainButton
          key={index}
          input={input}
          onClick={(event) => handleButtonClick(input, event)}
        />
      ))}
      <MainModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        content={modalContent}
        buttonPosition={buttonPosition}
        inputDiv={inputDiv}
      />
    </>
  );
}
