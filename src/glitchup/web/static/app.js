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

async function getFilter(filterID) {
  const filter = await fetch('/filters/' + filterID);
  const filterData = await filter.json();
  return filterData;
}

async function populate(filterID) {
  const filterJSON = await getFilter(filterID);
  const fileInputs = document.getElementById("fileInputs");
  const parameters = document.getElementById("parameters");
  fileInputs.innerHTML = `$(filterJSON.inputs)`;
  parameters.innerHTML = `$(filterJSON.parameters)`;
}

const inputs = document.getElementsByClassName("input");
for (let input of inputs) {
    input.addEventListener("change", function() {
        const filterID = input.id;
        populate(filterID).then(() => {
            console.log("populated");
        });
    });
}