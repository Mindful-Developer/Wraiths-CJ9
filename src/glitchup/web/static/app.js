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
  const filter = await fetch("/filters/" + filterID);
  const filterData = await filter.json();
  return filterData;
}

async function populate(filterID) {
  const filterJSON = await getFilter(filterID);
  const fileInputs = document.getElementById("fileInputs");
  const parameters = document.getElementById("parameters");
  fileInputs.innerHTML = `<header class="bg-success text-center py-2"><h3>Images</h3></header>`;
  fileInputs.innerHTML += `
            <div
            class="mb-5 m-4 d-flex flex-column justify-center"
            id="fileInput1"
          >
            <img id="frame1" src="" class="img-thumbnail d-none border-none" />
            <input
              class="form-control bg-dark text-dark border-secondary"
              type="file"
              id="formFile"
              onchange="preview()"
            />
            <button
              onclick="clearImage()"
              class="btn btn-danger mt-3 d-none"
              id="load1"
            >
              Remove
            </button>
          </div>
  `.repeat(filterJSON.inputs);
  parameters.innerHTML = `<header class="bg-success text-center py-2"><h3>Parameters</h3></header>`;
}

const inputs = document.getElementsByClassName("filter");
console.log(inputs);
for (let input of inputs) {
  input.addEventListener("change", () => {
    const filterID = input.id;
    console.log(filterID);
    populate(filterID);
  });
}
