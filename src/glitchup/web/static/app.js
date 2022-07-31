generateButton = document.getElementById("generate");

function preview() {
  const fileIn = document.getElementById("fileInput1").children;
  frame1.src = URL.createObjectURL(fileIn[1].files[0]);
  flipDisplay(fileIn);
}

function generateFlip(twoWay) {
  if (twoWay) {
    if (generateButton.hasAttribute("disabled")) {
      generateButton.removeAttribute("disabled");
    } else {
      generateButton.setAttribute("disabled", "");
    }
  } else {
    if (!generateButton.hasAttribute("disabled")) {
      generateButton.setAttribute("disabled", "");
    }
  }
}

function flipDisplay(fileIn) {
  for (let element of fileIn) {
    if (element.classList.contains("d-none")) {
      element.classList.remove("d-none");
    } else {
      element.classList.add("d-none");
    }
  }
  generateFlip(true);
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

function createRangeInput(min, max, defaultValue, paramName, smStep) {
  const range = document.createElement("div");
  range.innerHTML = `
  <div class="d-flex flex-column align-items-center my-2 text-center">
    <label for="${paramName}" class="form-label text-secondary">${paramName}</label>
    
    <div class="w-50 d-flex justify-content-center">
      <span class="h6 text-secondary me-2">${min}</span>
      <input class="form-range" id="${paramName}" type="range" min="${min}" max="${max}" value="${defaultValue}" step="${
    smStep ? "0.01" : "1"
  }"/>
      <span class="h6 text-secondary ms-2">${max}</span>
    </div>
    
  </div>
  `;
  return range;
}

function createDropdownInput(options, defaultValue) {
  const dropdown = document.createElement("select");
  dropdown.classList.add("bg-dark");
  dropdown.classList.add("text-light");
  dropdown.classList.add("my-2");
  dropdown.classList.add("form-select");
  dropdown.classList.add("w-50");
  for (let option of options) {
    const optionElement = document.createElement("option");
    optionElement.value = option;
    optionElement.innerHTML = option;
    dropdown.appendChild(optionElement);
  }
  dropdown.value = defaultValue;
  return dropdown;
}

async function populate(filterID) {
  generateFlip(false);
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
  for (let parameter of filterJSON.parameters) {
    if (parameter.type === "ENUM") {
      parameters.appendChild(
        createDropdownInput(parameter.range, parameter.default, parameter.name)
      );
    } else {
      parameters.appendChild(
        createRangeInput(
          parameter.range[0],
          parameter.range[1],
          parameter.default,
          parameter.name,
          parameter.type === "FLOAT" ? true : false
        )
      );
    }
  }
}

const inputs = document.getElementsByClassName("filter");
for (let input of inputs) {
  input.addEventListener("change", () => {
    const filterID = input.id;
    populate(filterID);
  });
}

function uuid4() {
    return ([1e7] + -1e3 + -4e3 + -8e3 + -1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

const canvas = document.getElementById("myCanvas");
generateButton.addEventListener("click", () => {

  const id = uuid4();
  form = document.getElementById("formSubmit");
  const formData = new FormData(form);
  formData.append("id", id);
  fetch("/images/add", {
    method: "POST",
    body: formData,
  });

  const downloadButton = document.getElementById("download");
  downloadButton.addEventListener("click", () => {
    downloadButton.setAttribute("href", `/images/${id}`);
    downloadButton.setAttribute("download", `${id}.png`);
  });

  const ws = new WebSocket("ws://localhost:8000/images/" + id);
  ws.onopen = () => {
    ws.send("");
  }
  ws.onmessage = (event) => {
    const image = new Image();
    image.src = event.data;
    image.onload = () => {
      canvas.width = image.width;
      canvas.height = image.height;
      canvas.getContext("2d").drawImage(image, 0, 0);
    }
  }
});
