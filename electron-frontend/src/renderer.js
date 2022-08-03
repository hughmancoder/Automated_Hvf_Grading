//imports
const { ipcRenderer } = require("electron");
const { PythonShell } = require("python-shell");
var path = require('path');

//variables
let overlay = document.getElementById("overlay");
let EToast = document.getElementById("Toast");
let Toast = new bootstrap.Toast(EToast);

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

let gradingdragFile = document.getElementById("gradingupload-box");
let gradinguploadbutton = document.getElementById("gradinguploadbuttonid");
let gradinguploadfolderbutton = document.getElementById(
  "gradinguploadfolderbuttonid"
);
let gradingImportStatus = document.getElementById("gradingpdflistid");
let loadingoutput = document.getElementById("loadingoutput");
let gradingdragcounter = 0;
let gradingjson;
let gradingdropfiles;

let analysisdragFile = document.getElementById("analysisupload-box");
let analysisuploadbutton = document.getElementById("analysisuploadbuttonid");
let analysisImportStatus = document.getElementById("analysispdflistid");
let analysisdragcounter = 0;
let analysisdropfiles;
let analysisjson;
let analysisimportjson;

let options = {
  mode: "text",
  pythonPath: path.join(__dirname, "/env/python.exe"),
  // pythonPath: "C:/Users/sonel/anaconda3/envs/newenv/python.exe",
  pythonOptions: ["-u"], // get print results in real-time
  scriptPath: __dirname,
};

// Grading Listeners
gradingdragFile.addEventListener("dragover", function (e) {
  e.preventDefault();
  e.stopPropagation();
});

gradingdragFile.addEventListener("dragenter", function () {
  showDropZone();
  gradingdragcounter++;
  //console.log("File has entered the Drop Space");
});

gradingdragFile.addEventListener("dragleave", function () {
  gradingdragcounter--;
  if (gradingdragcounter === 0) {
    hideDropZone();
  }

  //console.log("File has left the Drop Space");
});

gradingdragFile.addEventListener("drop", function (e) {
  e.preventDefault();
  e.stopPropagation();
  gradingupdatefilecounter(e.dataTransfer.files);
  gradingdropfiles = e.dataTransfer.files;
  hideDropZone();
});

gradinguploadbutton.addEventListener(
  "change",
  function (e) {
    gradingupdatefilecounter(gradinguploadbutton.files);
  },
  false
);

gradinguploadfolderbutton.addEventListener(
  "change",
  function (e) {
    gradingupdatefilecounter(gradinguploadfolderbutton.files);
  },
  false
);

// Analysis Listeners

analysisdragFile.addEventListener("dragover", function (e) {
  e.preventDefault();
  e.stopPropagation();
});

analysisdragFile.addEventListener("dragenter", function () {
  showDropZone();
  analysisdragcounter++;
  //console.log("File has entered the Drop Space");
});

analysisdragFile.addEventListener("dragleave", function () {
  analysisdragcounter--;
  if (analysisdragcounter === 0) {
    hideDropZone();
  }

  //console.log("File has left the Drop Space");
});

analysisdragFile.addEventListener("drop", function (e) {
  e.preventDefault();
  e.stopPropagation();
  analysisupdatefilecounter(e.dataTransfer.files);
  analysisdropfiles = e.dataTransfer.files;
  hideDropZone();
});

analysisuploadbutton.addEventListener(
  "change",
  function () {
    analysisupdatefilecounter(analysisuploadbutton.files);
  },
  false
);

// Common Listeners
document.querySelectorAll(".nav-item").forEach((tab) => {
  tab.addEventListener("click", function (e) {
    e.preventDefault();
    if (tab.id == "tab-1") {
      document.body.style.backgroundImage =
        "linear-gradient(90deg, #019B93, #5e62b0, #ce5289)";
    } else if (tab.id == "tab-2") {
      document.body.style.backgroundImage =
        "linear-gradient(90deg, #48B86F, #4CAC9A, #2780BB)";
    }
    else if (tab.id == "tab-3") {
      document.body.style.backgroundImage =
        "linear-gradient(90deg, #E45454, #AD3AAD, #7C36AA)";
    }
    else if (tab.id == "tab-4") {
      document.body.style.backgroundImage =
        "linear-gradient(90deg, #C49234, #B057C7, #C45252)";
    }
  });
});

// general functions

function hideDropZone() {
  gradingdragFile.classList.remove("bg-success");
}

function showDropZone() {
  gradingdragFile.classList.add("bg-success");
}

/**
 * Enables Overlay
 */
async function LoadingOn() {
  overlay.classList.add("show");
  overlay.classList.remove("hide");
}

/**
 * Disables Overlay
 */
async function LoadingOff() {
  overlay.classList.add("hide");
  overlay.classList.remove("show");
  document.getElementById("loadingprogress").ariaValueNow = 0;
  document.getElementById("loadingprogress").style.width = "0%";
  document.getElementById("loadingtimeleft").textContent = "";
  loadingoutput.textContent = "";
}

async function OpenDevTools() {
  ipcRenderer.send("openDevTools");
}

// grading functions

/**
 * Validates Grading Files
 */
async function gradingsubmitButton() {
  await LoadingOn();
  if (gradinguploadbutton.files.length >= 1) {
    await gradinguploadfiles(gradinguploadbutton.files);
  } else if (gradinguploadfolderbutton.files.length >= 1) {
    await gradinguploadfiles(gradinguploadfolderbutton.files);
  } else if (gradingdropfiles && gradingdropfiles.length >= 1) {
    await gradinguploadfiles(gradingdropfiles);
  } else {
    EToast.children[1].children[0].textContent = "No Files Added";
    Toast.show();
    await LoadingOff();
  }
}

/**
 * Clears Grading Page
 */
async function gradingclearButton() {
  gradingImportStatus.textContent = "Files or Folder(s) accepted";
  gradingImportStatus.classList.remove("text-success");
  gradinguploadbutton.value = "";
  gradinguploadfolderbutton.value = "";

  $("#gradingtable-div").empty();
  gradingjson = null;
}

/**
 * Updates the grading file counter
 * @param {FileList} files
 */
async function gradingupdatefilecounter(files) {
  await LoadingOn();

  let counter = 0;
  const acceptedImageTypes = [
    "application/pdf",
    "image/png",
    "image/bmp",
    "image/jpg",
    "image/jpeg",
  ];
  for await (let f of files) {
    if (acceptedImageTypes.includes(f.type)) {
      counter++;
    }
    gradingImportStatus.textContent = counter + " Files added";
    gradingImportStatus.classList.add("text-success");
  }

  await LoadingOff();
}

/**
 * Grades Files
 * @param {FileList} files
 */
async function gradinguploadfiles(files) {
  await LoadingOn();
  let array = [];
  array.push("-f");

  await Array.from(files).reduce(async (promise, f) => {
    await promise;
    array.push(f.path);
  }, Promise.resolve());

  options.args = array;

  let pyshell = new PythonShell("pythonscript.py", options);
  await gradingclearButton();
  let errorcount = 0;

  pyshell.on("message", function (message) {
    if (message.startsWith("Error:")) {
      errorcount++;
      console.log(message);
    } else if (message.startsWith("Info:")) {
      let info = message;
      info = info.replace("Info: ", "");
      loadingoutput.textContent = info;
    } else if (message.startsWith("<table")) {
      let content = document.getElementById("gradingtable-div");
      content.insertAdjacentHTML("afterbegin", message);
      $('#grading-table > thead > tr').children().eq(4).attr({"data-field":"Eye", "data-filter-control":"select", "data-sortable":true});
      $('#grading-table > thead > tr').children().eq(3).attr({"data-field":"ID", "data-filter-control":"select", "data-sortable":true});
      $('#grading-table > thead > tr').children().eq(1).attr({"data-field":"Name", "data-filter-control":"select", "data-sortable":true});
      
      $('#grading-table').attr({"data-search":true, "data-single-select":true, "data-click-to-select":true,  "data-show-columns":true, "data-show-columns-search":true, "data-search-highlight":true, "data-show-columns-toggle-all":true, 
      "data-buttons-align":"left", "data-show-export":true, "data-filter-control":true, "data-silent-sort":false, "data-alignment-select-control-options":"left", "data-disable-control-when-search":true,
      "data-show-search-clear-button":true});
      
      $('#grading-table > thead > tr').prepend('<th data-field="radio" data-radio="true"></th>')
      $('#grading-table > tbody > tr').prepend('<td></td>')
      
      $('#grading-table').bootstrapTable();
      console.log(message);
    } else if (message.startsWith('{"schema')) {
      gradingjson = null;
      gradingjson = JSON.parse(message);
      console.log(message);
    } else if (message.startsWith("Progress:")) {
      let progress = message;
      progress = progress.replace("Progress: ", "");
      document.getElementById("loadingprogress").ariaValueNow = progress;
      document.getElementById("loadingprogress").style.width = progress + "%";
      console.log(progress + "%");
    } else if (message.startsWith("ETA:")) {
      document.getElementById("loadingtimeleft").textContent = message;
      console.log(message);
    } else {
      console.log(message);
    }
  });

  pyshell.on("pythonError", function (error) {
    console.log(error);
    errorcount++;
    LoadingOff();
  });

  pyshell.end(function (err, code, signal) {
    if (err) console.log(err);
    LoadingOff();
    EToast.children[1].children[0].textContent = errorcount + " errors occured";
    Toast.show();
  });
}

/**
 * Exports data from Grading to Analysis
 */
async function gradingExportToProgression() {
  LoadingOn();
  if (gradingjson != null) {
    analysisimportjson = gradingjson;
    document.getElementById("analysis-tab").click();
    analysisImportStatus.textContent = "Data From Grading Imported";
    analysisImportStatus.classList.add("text-success");
  } else {
    EToast.children[1].children[0].textContent = "No data to process";
    Toast.show();
  }
  LoadingOff();
}

// Analysis Functions

/**
 * Imports data from Grading to Analysis
 */
async function ImportFromGrading() {
  LoadingOn();
  if (gradingjson != null) {
    analysisimportjson = gradingjson;
    analysisImportStatus.textContent = "Data From Grading Imported";
    analysisImportStatus.classList.add("text-success");
  } else {
    EToast.children[1].children[0].textContent = "No data to process";
    Toast.show();
  }
  LoadingOff();
}

/**
 * Validates Analysis Files
 */
async function analysissubmitButton() {
  await LoadingOn();
  if (analysisuploadbutton.files.length >= 1) {
    await analysisuploadfiles(analysisuploadbutton.files[0].path, "csv");
  } else if (analysisdropfiles && analysisdropfiles.length >= 1) {
    await analysisuploadfiles(analysisdropfiles[0].path, "csv");
  } 
  else if(analysisimportjson != null){
    await analysisuploadfiles(analysisimportjson, "json");
  }
  else {
    EToast.children[1].children[0].textContent = "No Files Added";
    Toast.show();
    await LoadingOff();
  }
}

/**
 * Clears the analysis page
 */
async function analysisclearButton() {
  analysisImportStatus.textContent = "CSV accepted";
  analysisImportStatus.classList.remove("text-success");
  analysisuploadbutton.value = "";

  $("#analysistable-div").empty();
  analysisjson = null;
  analysisimportjson = null;

}

/**
 * Updates the Analysis file counter
 * @param {FileList} files
 */
async function analysisupdatefilecounter(files) {
  await LoadingOn();

  // let counter = 0;
  const acceptedImageTypes = ["text/csv", "application/vnd.ms-excel"];

  if (acceptedImageTypes.includes(files[0].type)) {
    // counter++;
    analysisImportStatus.textContent = "CSV Uploaded"
    analysisImportStatus.classList.add("text-success");
  }

  // analysispdflist.textContent = counter + " Files added";

  await LoadingOff();
}

/**
 * Start Analysis
 * @param {string} inputdf
 */
async function analysisuploadfiles(inputdf, format) {
  await LoadingOn();

  let array = ["-g"];
  if (document.getElementById("analysisidradio").checked) {
    array.push("0");
  } else if (document.getElementById("analysisfolderradio").checked) {
    array.push("1");
  } else {
    array.push("0");
  }

  array.push("-p"); 

  let selected = document.getElementById('analysisDropdown');

  array.push(selected.options[selected.selectedIndex].value);

  if(format == "json"){
    array.push("-j");
    array.push(JSON.stringify(inputdf));
  }
  else if(format == "csv"){
    array.push("-c");
    array.push(inputdf);
  }

  options.args = array;

  let pyshell = new PythonShell("pythonscript.py", options);
  await analysisclearButton();
  let errorcount = 0;
  
  pyshell.on("message", function (message) {
    if (message.startsWith("Error:")) {
      errorcount++;
      console.log(message);
    } else if (message.startsWith("Info:")) {
      let info = message;
      info = info.replace("Info: ", "");
      loadingoutput.textContent = info;
    } else if (message.startsWith("<table")) {
      let content = document.getElementById("analysistable-div");
      content.insertAdjacentHTML("afterbegin", message);
      $('#analysis-table > thead > tr').children().eq(4).attr({"data-field":"Eye", "data-filter-control":"select", "data-sortable":true});
      $('#analysis-table > thead > tr').children().eq(3).attr({"data-field":"ID", "data-filter-control":"select", "data-sortable":true});
      $('#analysis-table > thead > tr').children().eq(1).attr({"data-field":"Name", "data-filter-control":"select", "data-sortable":true});
      $('#analysis-table').attr({"data-search":true, "data-single-select":true, "data-click-to-select":true,  "data-show-columns":true, "data-show-columns-search":true, "data-search-highlight":true, "data-show-columns-toggle-all":true,
      "data-buttons-align":"left", "data-show-export":true, "data-filter-control":true, "data-silent-sort":false, "data-alignment-select-control-options":"left", "data-disable-control-when-search":true,
      "data-show-search-clear-button":true});
      $('#analysis-table > thead > tr').prepend('<th data-field="radio" data-radio="true"></th>')
      $('#analysis-table').bootstrapTable();
      console.log(message);
    } else if (message.startsWith('{"schema')) {
      analysisjson = null;
      analysisjson = JSON.parse(message);
    } else if (message.startsWith("Progress:")) {
      let progress = message;
      progress = progress.replace("Progress: ", "");
      document.getElementById("loadingprogress").ariaValueNow = progress;
      document.getElementById("loadingprogress").style.width = progress + "%";
      console.log(progress + "%");
    } else if (message.startsWith("ETA:")) {
      document.getElementById("loadingtimeleft").textContent = message;
      console.log(message);
    } else {
      console.log(message);
    }
  });

  pyshell.on("pythonError", function (error) {
    console.log(error);
    errorcount++;
    LoadingOff();
  });

  pyshell.end(function (err, code, signal) {
    if (err) {
      errorcount++;
      console.log(err);
    }
    LoadingOff();
    EToast.children[1].children[0].textContent = errorcount + " errors occured";
    Toast.show();
  });
}