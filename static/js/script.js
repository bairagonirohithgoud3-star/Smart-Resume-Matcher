const resumeInput = document.getElementById("resume");
const fileLabel = document.getElementById("file-label");
const form = document.getElementById("resume-form");
if (resumeInput && fileLabel) {
  resumeInput.addEventListener("change", () => {
    if (resumeInput.files.length) {
      const file = resumeInput.files[0];
      fileLabel.textContent = file.name;
      if (file.size > 5 * 1024 * 1024) {
        fileLabel.textContent = "File is too large — choose a file under 5 MB";
        resumeInput.value = "";
      }
    }
  });
}
if (form) {
  form.addEventListener("submit", (event) => {
    if (!resumeInput.files.length) {
      event.preventDefault();
      alert("Please choose your resume first.");
    }
  });
}
