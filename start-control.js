// This function triggers only once when javascript is first loaded
setTimeout(function loadPageLoop(){
    // remove splash screen here
    document.getElementById("splash-screen").style.transition = "opacity 1s linear";
    document.getElementById("splash-screen").style.opacity = "0";
    setTimeout(function clearSplash(){
        document.getElementById("splash-screen").style.display = "none";
    }, 2000);

    pywebview.api.initRunLoop();
    pywebview.api.getAllSequences('dict').then(refreshSeqList);
    mainLoop()
}, 1000);


// page load/refresh loop (displays new changes to the json)
function mainLoop() {
    setTimeout(function runner() {
        //pywebview.api.getAllSequences('dict').then(refreshSeqList);
        pywebview.api.mainRunLoop();
        mainLoop();
    }, 1000);
}

function refreshTable() {
    pywebview.api.getAllSequences('dict').then(refreshSeqList);
}

function refreshSeqList(response){
    const objArr = JSON.parse(response.allSeqJson);
    var table = document.getElementById("allSeqTableBody");
    table.innerHTML = "";

    // loop through all seq files to add
    for (let i = 0; i < objArr.length; i++) {
        var row = table.insertRow(0);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = objArr[i][0];
        cell1.setAttribute("onclick", "openSeq('"+objArr[i][0]+"')");
        cell1.setAttribute("title", "Open and start editing the sequence")
        cell2.innerHTML = objArr[i][1];
        cell2.setAttribute("onclick", "modifyJsonValue('"+objArr[i][0]+"','editEnable','"+objArr[i][1]+"')");
        cell2.setAttribute("title", "Turn on/off the sequence")
        cell3.innerHTML = objArr[i][2];
        cell3.setAttribute("onclick", "modifyJsonValue('"+objArr[i][0]+"','editTriggerInit','"+objArr[i][2]+"')");
        cell3.setAttribute("title", "Set an event that can start the sequence")
        cell4.innerHTML = objArr[i][3];
        cell4.setAttribute("onclick", "modifyJsonValue('"+objArr[i][0]+"','editOutcomeInit','"+objArr[i][3]+"')");
        cell4.setAttribute("title", "Connect sequences together")
    }
}

function openSeq(seqName) {
    pywebview.api.openSequence(seqName).then(showLoadErrors);
}

function cancelEdit() {
    document.getElementById("overlay-trigger-chose").style.display = "none";
    document.getElementById("overlay-trigger-button").style.display = "none";
    document.getElementById("overlay-trigger-time").style.display = "none";
    document.getElementById("overlay-outcome-chose").style.display = "none";
    document.getElementById("overlay-outcome-runseq").style.display = "none";
    document.getElementById("overlay-export").style.display = "none";
    document.getElementById("overlay-delete").style.display = "none";
    document.getElementById("overlay").style.display = "none";
}
function cancelAlert() {
    document.getElementById("overlay-message").style.display = "none";
}

function initTimeTriggerInput() {
    document.getElementById("overlay-trigger-chose").style.display = "none";
    document.getElementById("overlay-trigger-button").style.display = "none";
    document.getElementById("overlay-trigger-time").style.display = "block";
}
function initButtonTriggerInput () {
    document.getElementById("overlay-trigger-chose").style.display = "none";
    document.getElementById("overlay-trigger-button").style.display = "block";
    document.getElementById("overlay-trigger-time").style.display = "none";
}
function initOutcomeSuccess () {
    document.getElementById("overlay-outcome-chose").style.display = "none";
    document.getElementById("overlay-outcome-runseq").style.display = "block";
    document.getElementById("outcomeSuccessAccept").style.display = "inline-block";
    document.getElementById("outcomeUnsuccessAccept").style.display = "none";
}
function initOutcomeUnsuccess () {
    document.getElementById("overlay-outcome-chose").style.display = "none";
    document.getElementById("overlay-outcome-runseq").style.display = "block";
    document.getElementById("outcomeSuccessAccept").style.display = "none";
    document.getElementById("outcomeUnsuccessAccept").style.display = "inline-block";
}

function modifyJsonValue(seqName, type, value) {
    if (type == "editEnable") {
        if (value == "true") {
            statusToSet = "false";
        }
        if (value == "false") {
            statusToSet = "true";
            pywebview.api.initRunLoop();
        }
        pywebview.api.changeJsonInteraction(seqName, statusToSet, 'seqEnabled');
        refreshTable();
    }
    if (type == "editTriggerInit") {
        document.getElementById("overlay-trigger-chose").style.display = "block";
        cacheSeqName = seqName;
    }
    if (type == "trigger-time") {
        var textInput = document.getElementById("loopTime");
        if (!textInput.checkValidity() && textInput.value != "") {
            // not valid
            alertMessageLocal("Invalid input!");
            return;
        }
        else {
            if (value == "") {
                return;
            }
            value = "Every " + value + " seconds";
            pywebview.api.changeJsonInteraction(cacheSeqName, value, 'trigger');
            pywebview.api.initRunLoop();
            refreshTable();
        }
    }
    if (type == "trigger-button") {
        pywebview.api.changeJsonInteraction(cacheSeqName, value, 'trigger');
        refreshTable();
    }

    if (type == "editOutcomeInit") {
        document.getElementById("overlay-outcome-chose").style.display = "block";
        cacheSeqName = seqName;
    }
    if (type == "outcome-run-seq-success") {
        document.getElementById("overlay-outcome-chose").style.display = "none";
        var textInput = document.getElementById("textInputField");
        if (!textInput.checkValidity() && textInput.value != "") {
            alertMessageLocal("Invalid input!");
            return;
        }
        else {
            if (value == "") {
                return;
            }
            value = "Success -> " + value;
            pywebview.api.changeJsonInteraction(cacheSeqName, value, 'outcome');
            refreshTable();
        }
    }
    if (type == "outcome-run-seq-unsuccess") {
        document.getElementById("overlay-outcome-chose").style.display = "none";
        var textInput = document.getElementById("textInputField");
        if (!textInput.checkValidity() && textInput.value != "") {
            alertMessageLocal("Invalid input!");
            return;
        }
        else {
            if (value == "") {
                return;
            }
            value = "Failure -> " + value;
            pywebview.api.changeJsonInteraction(cacheSeqName, value, 'outcome');
            refreshTable();
        }
    }
    if (type == "trigger-delete") {
        document.getElementById("overlay-trigger-chose").style.display = "none";
        pywebview.api.changeJsonInteraction(cacheSeqName, 'null', 'trigger');
        refreshTable();
    }
    if (type == "outcome-delete") {
        document.getElementById("overlay-outcome-chose").style.display = "none";
        pywebview.api.changeJsonInteraction(cacheSeqName, 'null', 'outcome');
        refreshTable();
    }
}

function alertResponse(response){
    alertMessageLocal("Error:<br>" + response.message);
}

function inputNewSeq() {
    document.getElementById("overlay").style.display = "block";
}

function cancelInputNewSeq() {
    document.getElementById("overlay").style.display = "none";
}

function confirmInputNewSeq() {
    var textInput = document.getElementById("seqNameInputField");
    if (textInput.checkValidity()) {
        // name allowed.
        document.getElementById("overlay").style.display = "none";
        refreshTable();
        pywebview.api.newSequence(textInput.value).then(alertResponse);
        pywebview.api.getAllSequences('dict').then(refreshSeqList);
    } else {
        alertMessageLocal("Invalid name!<br>Only alphanumeric characters, underscore, space and dash allowed.<br>Maximum length is 30 characters.");
    }
}

function showLoadErrors(response) {

    if (response.errorMissingFiles != null) {
        // there are missing files!
        var missingFilesJson = response.errorMissingFiles;
        var missingFilesStr = missingFilesJson.replace("[", "").replace("]", "");
        alertMessageLocal("ERROR<br>The following files are missing in the sequence:<br>"+missingFilesStr);
        return;
    }
}

function importSequence() {
    pywebview.api.importSequence().then(refreshSeqList);
}

function deleteSeqMenu() {
    document.getElementById("overlay-delete").style.display = "block";
    pywebview.api.getAllSequences('dict').then(refreshDelTable);
}
function manRefreshSeqMenu() {
    refreshTable();
}

function exportSeqMenu() {
    document.getElementById("overlay-export").style.display = "block";
    pywebview.api.getAllSequences('dict').then(refreshExportTable);
}

function refreshDelTable(response) {
    const objArr = JSON.parse(response.allSeqJson);
    //alert(response.allSeqJson);
    var tableDel = document.getElementById("delSeqTableBody");
    tableDel.innerHTML = "";
    // loop through all seq files to add
    for (let i = 0; i < objArr.length; i++) {
        var row = tableDel.insertRow(0);
        var cell1 = row.insertCell(0);
        cell1.innerHTML = objArr[i][0];
        cell1.setAttribute("onclick", "delSeq('"+objArr[i][0]+"')");
    }
    refreshTable();
}

function refreshExportTable(response) {
    const objArr = JSON.parse(response.allSeqJson);
    //alert(response.allSeqJson);
    var tableDel = document.getElementById("exportSeqTableBody");
    tableDel.innerHTML = "";
    // loop through all seq files to add
    for (let i = 0; i < objArr.length; i++) {
        var row = tableDel.insertRow(0);
        var cell1 = row.insertCell(0);
        cell1.innerHTML = objArr[i][0];
        cell1.setAttribute("onclick", "exportSeq('"+objArr[i][0]+"')");
    }
}

function delSeq(seqToDelete) {
    pywebview.api.delSequence(seqToDelete).then(refreshDelTable);
}
function exportSeq(seqToExport) {
    pywebview.api.exportSequence(seqToExport);
    document.getElementById("overlay-export").style.display = "none";
}

function openHelp() {
    pywebview.api.openHelp();
}

function openCredits() {
    pywebview.api.openCredits();
}

function alertMessageLocal(message) {
    var message = String(message);
    document.getElementById("overlay-message").style.display = "block";
    document.getElementById("messageAlert").innerHTML = message + "<br><br>";
}