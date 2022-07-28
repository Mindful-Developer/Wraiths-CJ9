function preview() {
  const fileIn = document.getElementById("fileInput1").children;
  frame1.src = URL.createObjectURL(fileIn[1].files[0]);
  flipDisplay(fileIn);
}

function flipDisplay(fileIn) {
  for (let element of fileIn) {
    if (element.classList.contains("d-none")) {
      element.classList.remove("d-none");
    } else {
      element.classList.add("d-none");
    }
  }
}

function clearImage() {
  const fileIn = document.getElementById("fileInput1").children;
  document.getElementById("formFile").value = null;
  frame1.src = "";
  flipDisplay(fileIn);
}
