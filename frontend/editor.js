require.config({
  paths: {
    vs: 'https://unpkg.com/monaco-editor@0.45.0/min/vs'
  }
});

require(['vs/editor/editor.main'], function () {

  const editor = monaco.editor.create(
    document.getElementById('editor'),
    {
      value: `public class Main { 

  public static void main(String[] args) {

  }

}`,
      language: 'java',
      theme: 'vs-dark',
      automaticLayout: true
    }
  );

  const modal = document.getElementById("pythonModal");
  const textarea = document.getElementById("pythonInput");
  const translateBtn = document.getElementById("translateBtn");
  const cancelBtn = document.getElementById("cancelBtn");

  let insertPosition = null;

  // CTRL + ENTER opens modal
  editor.addCommand(
    monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
    function () {
      insertPosition = editor.getPosition();
      textarea.value = "";
      modal.style.display = "block";
      textarea.focus();
    }
  );

  // Cancel button
  cancelBtn.onclick = function () {
    modal.style.display = "none";
  };

  // Translate button
  translateBtn.onclick = function () {

    const pythonCode = textarea.value;

    if (!pythonCode.trim()) return;

    fetch("/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: pythonCode })
    })
    .then(res => res.json())
    .then(data => {

      if (!data.java_code.startsWith("//")) {
        insertJavaAtCursor(data.java_code);
      }

      modal.style.display = "none";
    });
  };


  function insertJavaAtCursor(javaCode) {

    const model = editor.getModel();

    model.applyEdits([{
      range: new monaco.Range(
        insertPosition.lineNumber,
        insertPosition.column,
        insertPosition.lineNumber,
        insertPosition.column
      ),
      text: "\n" + javaCode + "\n"
    }]);
  }
  const runBtn = document.getElementById("runBtn");
const consoleOutput = document.getElementById("console");

runBtn.onclick = function () {

  const javaCode = editor.getValue();

  fetch("/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ code: javaCode })
  })
  .then(res => res.json())
  .then(data => {
    consoleOutput.textContent = data.output;
  });
};
     
});