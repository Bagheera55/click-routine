
function showResponse(response) {
    // this is an async callback function, needed by all ".then"-methods.
    var container = document.getElementById('response-container')

    container.innerText = response.message
    container.style.display = 'block'
}

function alertTest(text) {
    alert("this is your input:" +text);
}

// Wait for page to load first time.
setTimeout(function loadPageLoop(){
    pywebview.api.getJsonLoaded().then(refreshJson);
    cancelInputNewSeq(); // set some css properties, in order to display edit menu correctly
}, 200);


function refreshJson(response) {
    function isOdd(num) { return num % 2;}

    seqName = response.activeFile.replace(/^.*[\\\/]/, '').split('.')[0]; // removing full filepath and extension
    document.getElementById("header").innerHTML = seqName;

    // remove all actions with jsonLoadedEntry as class name
    var list = document.getElementsByClassName("column-seq jsonLoadedEntry");
    for(var i = list.length - 1; 0 <= i; i--)
    if(list[i] && list[i].parentNode)
        list[i].parentNode.removeChild(list[i]);

    seqArray = response.jsonSequence;

    for (var i = 0; i < seqArray.length; i++){
        var obj = seqArray[i];

        if (obj["type"]) {
            var actionPosition = i + 1;

            // Converting everything to strings in order to make div.setAttribute simpler and simplifies upcoming function handling
            editActionViewFull = `editActionView( ${actionPosition},
                            \"${obj['type']}\",
                            \"${obj['location']}\",
                            \"${obj['content']}\",
                            \"${obj['wait']}\",
                            \"${obj['moveToPositionSuccess']}\",
                            \"${obj['moveToPositionFail']}\",
                            \"${obj['confidence']}\",
                            \"${obj['adjustX']}\",
                            \"${obj['adjustY']}\")`;

            if (obj["type"] == "capture") {
                //Assuming image always exists in this code
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundImage = "url('data:image/png;base64," + obj["location"] + "')";
                div.style.backgroundRepeat = "no-repeat";
                div.style.backgroundPosition = "center center";
                div.style.backgroundColor = "rgba(0, 0, 40, 0.5)";
                div.style.border = "1px solid black";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline  = "8px solid rgba(0, 0, 0, .08)";
                }

                // time delay arrow
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundImage = "url('assets/icons/Arrow-Right.png')";
                div.style.backgroundRepeat = "no-repeat";
                div.style.backgroundPosition = "center center";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.paddingTop = "100px";
                div.innerHTML = "<b>Wait:</b><br>" + obj["wait"] + " sec";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline = "8px solid rgba(0, 0, 0, .08)";
                    div.style.backgroundColor = "rgba(0, 0, 0, .08)";
                }
            }
            if (obj["type"] == "text") {
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundColor = "rgba(0, 40, 0, 0.5)";
                div.style.border = "1px solid black";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.color = "GhostWhite";
                div.innerHTML = "<br><b>Text type:</b><br><i>" + obj["content"] + "</i>";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline  = "8px solid rgba(0, 0, 0, .08)";
                }

                // time delay arrow
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundImage = "url('assets/icons/Arrow-Right.png')";
                div.style.backgroundRepeat = "no-repeat";
                div.style.backgroundPosition = "center center";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.paddingTop = "100px";
                div.innerHTML = "<b>Wait:</b><br>" + obj["wait"] + " sec";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline = "8px solid rgba(0, 0, 0, .08)";
                    div.style.backgroundColor = "rgba(0, 0, 0, .08)";
                }
            }

            if (obj["type"] == "special") {
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundColor = "rgba(40, 120, 80, 0.5)";
                div.style.border = "1px solid black";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.color = "GhostWhite";
                div.innerHTML = "<br><b>Key press:</b><br><i>" + obj["content"] + "</i>";
                document.getElementById("seqGroup").insertBefore(div, newInputButton)
                if (isOdd(actionPosition)) {
                    div.style.outline  = "8px solid rgba(0, 0, 0, .08)";
                };

                // time delay arrow
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundImage = "url('assets/icons/Arrow-Right.png')";
                div.style.backgroundRepeat = "no-repeat";
                div.style.backgroundPosition = "center center";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.paddingTop = "100px";
                div.innerHTML = "<b>Wait:</b><br>" + obj["wait"] + " sec";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline = "8px solid rgba(0, 0, 0, .08)";
                    div.style.backgroundColor = "rgba(0, 0, 0, .08)";
                }
            }
            if (obj["type"] == "position") {
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundColor = "rgba(40, 0, 60, 0.5)";
                div.style.border = "1px solid black";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.color = "GhostWhite";
                div.innerHTML = "<br><b>Click Position:</b><br><i>" + obj["location"] + "</i>";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline  = "8px solid rgba(0, 0, 0, .08)";
                }

                // time delay arrow
                var div = document.createElement("div");
                div.className = "column-seq jsonLoadedEntry";
                div.setAttribute("onclick", editActionViewFull);
                div.style.backgroundImage = "url('assets/icons/Arrow-Right.png')";
                div.style.backgroundRepeat = "no-repeat";
                div.style.backgroundPosition = "center center";
                div.style.textAlign = "center";
                div.style.fontSize = "20px";
                div.style.paddingTop = "100px";
                div.innerHTML = "<b>Wait:</b><br>" + obj["wait"] + " sec";
                document.getElementById("seqGroup").insertBefore(div, newInputButton);
                if (isOdd(actionPosition)) {
                    div.style.outline = "8px solid rgba(0, 0, 0, .08)";
                    div.style.backgroundColor = "rgba(0, 0, 0, .08)";
                }
            }
        }
    }
}

function newInputButtonPress() {
    document.getElementById("overlay-input-menu").style.display = "block";
}

function cancelInputNewSeq() {
    document.getElementById("overlay-input-menu").style.display = "none";
    document.getElementById("overlay-text").style.display = "none";
    document.getElementById("overlay-special").style.display = "none";
    document.getElementById("overlay-action-edit").style.display = "none";
    document.getElementById("overlay-global-seq-settings").style.display = "none";
    document.getElementById("hidy-clickboxes").style.display = "none";
    document.getElementById("hidy-captureSettings").style.display = "none";
    document.getElementById("overlay-clear-confirm").style.display = "none";
}

function cancelOverlayMessage() {
    document.getElementById("overlay-message").style.display = "none";
}

function inputTextView() {
    document.getElementById("overlay-input-menu").style.display = "none";
    document.getElementById("overlay-text").style.display = "block";
    document.getElementById("ConfirmInputButton").style.display = "inline-block";
    document.getElementById("hidden-edit-text-confirm-button").style.display = "none";
}

function inputSpecialView() {
    document.getElementById("overlay-input-menu").style.display = "none";
    document.getElementById("overlay-special").style.display = "block";
}

function confirmInputText() {
    var textInput = document.getElementById("textInputField");
    if (textInput.checkValidity()) {
        // name allowed.
        document.getElementById("overlay-input-menu").style.display = "none";
        document.getElementById("overlay-text").style.display = "none";
        pywebview.api.addTextToJson(textInput.value, null).then(refreshJson);
    } else {
        alertMessageLocal("Invalid text! Double quote and backslash are not allowed. Maximum length is 300 characters.");
    }
}

function confirmInputSpecial(value) {
    document.getElementById("overlay-input-menu").style.display = "none";
    document.getElementById("overlay-special").style.display = "none";
    pywebview.api.addSpecialToJson(value, null).then(refreshJson);
}

function newCaptureClick() {
    pywebview.api.screenCapture().then(parseCapture);
    document.getElementById("overlay-input-menu").style.display = "none";
}
function newPositionClick() {
    pywebview.api.screenPosition().then(parsePosClick);
    document.getElementById("overlay-input-menu").style.display = "none";
}

function parseCapture(response) {
    pywebview.api.addCaptureToJson(response.location, null).then(refreshJson);
}
function parsePosClick(response) {
    pywebview.api.addPosClickToJson(response.clickXyPos, null).then(refreshJson);
}

function openClearConfirmWindow() {
    document.getElementById("overlay-clear-confirm").style.display = "block";
}
function clearSeq() {
    pywebview.api.clearCurrentSeq().then(refreshJson);
    document.getElementById("overlay-clear-confirm").style.display = "none";
}

function runSeq() {
    pywebview.api.runSeq("current").then(alertRun);
}

function editActionView(id,type,location,content,wait,moveToPositionSuccess,moveToPositionFail,confidence,adjustX,adjustY) {
    document.getElementById("overlay-action-edit").style.display = "block";
    document.getElementById("editingModeDisplayId").innerHTML = "Position: "+ id;
    document.getElementById("confidenceSelectBox").value = confidence;
    document.getElementById("moveToPositionSuccess").value = moveToPositionSuccess;
    document.getElementById("moveToPositionFail").value = moveToPositionFail;
    document.getElementById("adjustX").value = adjustX;
    document.getElementById("adjustY").value = adjustY;
    document.getElementById("delayTime").value = wait;
    document.getElementById("singleclick").checked = false;
    document.getElementById("doubleclick").checked = false;
    document.getElementById("tripleclick").checked = false;

    if (moveToPositionSuccess == "null") {
        document.getElementById("moveToPositionSuccess").value = "";
    }
    if (moveToPositionFail == "null") {
        document.getElementById("moveToPositionFail").value = "";
    }
    if (adjustX == "null") {
        document.getElementById("adjustX").value = "";
    }
    if (adjustY == "null") {
        document.getElementById("adjustY").value = "";
    }

    if (content.includes("singleclick")) {
        document.getElementById("singleclick").checked = true;
        document.getElementById("doubleclick").checked = false;
        document.getElementById("tripleclick").checked = false;
        document.getElementById("noclick").checked = false;
    }
    if (content.includes("doubleclick")) {
        document.getElementById("singleclick").checked = false;
        document.getElementById("doubleclick").checked = true;
        document.getElementById("tripleclick").checked = false;
        document.getElementById("noclick").checked = false;
    }
    if (content.includes("tripleclick")) {
        document.getElementById("singleclick").checked = false;
        document.getElementById("doubleclick").checked = false;
        document.getElementById("tripleclick").checked = true;
        document.getElementById("noclick").checked = false;
    }
    if (content.includes("noclick")) {
        document.getElementById("singleclick").checked = false;
        document.getElementById("doubleclick").checked = false;
        document.getElementById("tripleclick").checked = false;
        document.getElementById("noclick").checked = true;
    }
    if (type == "text") {
        document.getElementById("hidden-edit-text-button").style.display = "block";
        document.getElementById("ConfirmInputButton").style.display = "none";
        document.getElementById("hidy-clickboxes").style.display = "none";
        document.getElementById("hidy-br").style.display = "block";
    }
    if (type == "capture") {
        document.getElementById("hidy-clickboxes").style.display = "block";
        document.getElementById("hidy-captureSettings").style.display = "block";
        document.getElementById("hidden-edit-text-button").style.display = "none";
        document.getElementById("hidy-br").style.display = "none";
    }
    if (type == "special") {
        document.getElementById("hidden-edit-text-button").style.display = "none";
        document.getElementById("hidy-clickboxes").style.display = "none";
        document.getElementById("hidy-captureSettings").style.display = "none";
        document.getElementById("hidy-br").style.display = "block";
    }
    if (type == "position") {
        document.getElementById("hidy-clickboxes").style.display = "block";
        document.getElementById("hidden-edit-text-button").style.display = "none";
        document.getElementById("hidy-captureSettings").style.display = "none";
        document.getElementById("hidy-br").style.display = "block";
    }

    // highlight selected ID
    document.getElementsByClassName('jsonLoadedEntry')[(id*2)-1].classList.add('actionHighlight');
    document.getElementsByClassName('jsonLoadedEntry')[(id*2)-2].classList.add('actionHighlight');
    setTimeout(function() {
        document.getElementsByClassName('jsonLoadedEntry')[(id*2)-1].classList.remove('actionHighlight');
        document.getElementsByClassName('jsonLoadedEntry')[(id*2)-2].classList.remove('actionHighlight');
    }, 500);
}

function multiJsonEdit(id, keyArray, valueArray) {
    // This function uses a timeout in order to not write multiple times at the same time to same file. Very necessary.
    function callEdit(id, key, value) {
        modifyJsonValue(id, key, value);
    }

    for (var i = 0; i < keyArray.length; i++) {
        var key = keyArray[i];
        var value = valueArray[i];
        setTimeout(callEdit, 100*i, id, key, value);
    }
}

function modifyJsonValue(id, key, value) {
    id = id.replace(/\D/g,'');  // get only the digit part of ID/pos.

    if (key == "wait") {
        var textInput = document.getElementById("delayTime");
        if (!textInput.checkValidity()) {
            // not valid
            alertMessageLocal("invalid delay");
            return;
        }
        else {
            pywebview.api.editJsonAction(id, key, value).then(refreshJson);
        }
    }
    if (key == "confidence") {
        var textInput = document.getElementById("confidenceSelectBox");
        if (!textInput.checkValidity()) {
            // not valid
            alertMessageLocal("invalid confidence value");
            return;
        }
        else {
            pywebview.api.editJsonAction(id, key, value).then(refreshJson);
        }
    }
    if (key == "content") {
        var textInput = document.getElementById("textInputField");
        if (!textInput.checkValidity()) {
            // not valid
            alertMessageLocal("Invalid text! Double quote and backslash are not allowed. Maximum length is 300 characters.");
        }
        else {
            cancelInputNewSeq();
            pywebview.api.editJsonAction(id, key, value).then(refreshJson);
        }
    }
    if (key == "typingspeed") {
        var textInput = document.getElementById("cpsSpeedField");
        if (!textInput.checkValidity()) {
            // not valid
            alertMessageLocal("Invalid value!");
        }
        else {
            cancelInputNewSeq();
            pywebview.api.editJsonAction("SETTINGS-change", "typingspeed", value).then(refreshJson);
        }
    }
    if (key == "seqtimeout") {
        var textInput = document.getElementById("seqTimeout");
        if (!textInput.checkValidity() && textInput.value != "") {
            // not valid
            alertMessageLocal("Invalid value!");
        }
        else {
            if (value == "") {
                value = "null";
            }
            cancelInputNewSeq();
            pywebview.api.editJsonAction("SETTINGS-change", "seqtimeout", value).then(refreshJson);
        }
    }
    if (key == "moveToPositionSuccess") {
        var textInputSuccess = document.getElementById("moveToPositionSuccess");
        if (/^[0-9]{1,10}$|^$/.test(textInputSuccess.value)) {
            // valid entry
            jumpv = textInputSuccess.value.replace(/\D/g,'');  // get only the digit part of ID/pos.
            if (jumpv == "") {
                jumpv = "null";
            }
            pywebview.api.editJsonAction(id, key, jumpv).then(refreshJson);
        }
        else {
            //  invalid
            alertMessageLocal("Invalid position");
            return;
        }
    }
    if (key == "moveToPositionFail") {
        var textInputFail = document.getElementById("moveToPositionFail");
        if (/^[0-9]{1,10}$|^$/.test(textInputFail.value)) {
            // valid entry
            jumpv = textInputFail.value.replace(/\D/g,'');  // get only the digit part of ID/pos.
            if (jumpv == "") {
                jumpv = "null";
            }
            pywebview.api.editJsonAction(id, key, jumpv).then(refreshJson);
        }
        else {
            // invalid
            alertMessageLocal("invalid position");
            return;
        }
    }
    if (key == "adjustX") {
        var adjustX = document.getElementById("adjustX");
        if (/^[0-9]{1,10}$|^-[0-9]{1,10}$|^$/.test(adjustX.value)) {
            // valid entry
            adjustX = adjustX.value;
            if (adjustX == "") {
                adjustX = "null";
            }
            pywebview.api.editJsonAction(id, key, adjustX).then(refreshJson);
        }
        else {
            // invalid
            alertMessageLocal("invalid number");
            return;
        }
    }
    if (key == "adjustY") {
        var adjustY = document.getElementById("adjustY");
        if (/^[0-9]{1,10}$|^-[0-9]{1,10}$|^$/.test(adjustY.value)) {
            // valid entry
            adjustY = adjustY.value;
            if (adjustY == "") {
                adjustY = "null";
            }
            pywebview.api.editJsonAction(id, key, adjustY).then(refreshJson);
        }
        else {
            // invalid
            alertMessageLocal("invalid number");
            return;
        }
    }

    if (key == "multiclick") {
        if (value == "singleclick") {
            document.getElementById("singleclick").checked = true;
            document.getElementById("doubleclick").checked = false;
            document.getElementById("tripleclick").checked = false;
            document.getElementById("noclick").checked = false;
        }
        if (value == "doubleclick") {
            document.getElementById("singleclick").checked = false;
            document.getElementById("doubleclick").checked = true;
            document.getElementById("tripleclick").checked = false;
            document.getElementById("noclick").checked = false;
        }
        if (value == "tripleclick") {
            document.getElementById("singleclick").checked = false;
            document.getElementById("doubleclick").checked = false;
            document.getElementById("tripleclick").checked = true;
            document.getElementById("noclick").checked = false;
        }
        if (value == "noclick") {
            document.getElementById("singleclick").checked = false;
            document.getElementById("doubleclick").checked = false;
            document.getElementById("tripleclick").checked = false;
            document.getElementById("noclick").checked = true;
        }
        pywebview.api.editJsonAction(id, "content", value).then(refreshJson);
    }
}

function moveAction(id, direction, steps) {
    id = id.replace(/\D/g,'');  // get only the digit part of ID.
    maxId = parseInt(document.getElementsByClassName('jsonLoadedEntry').length /2);

    if (id <= 1 && direction == "left") {
        return;
    }
    if (id >= maxId && direction == "right") {
        return;
    }

    if (direction == "left") {
        newId = parseInt(id) - steps;
        document.getElementById("editingModeDisplayId").innerHTML = "Position: " + newId;
    }
    if (direction == "right") {
        newId = parseInt(id) + steps;
        document.getElementById("editingModeDisplayId").innerHTML = "Position: " + newId;
    }

    pywebview.api.moveJsonAction(id, direction, steps).then(refreshJson);
}

function deleteAction(id) {
    id = id.replace(/\D/g,'');  // get only the digit part of ID.
    pywebview.api.deleteJsonAction(id).then(refreshJson);
}

function testAction(pos) {
    pos = pos.replace(/\D/g,'');  // get only the digit part of position.
    pywebview.api.testSeqPos(pos).then(alertMessage);
}

function alertMessage(response) {
    message = response.alertMessage;
    document.getElementById("overlay-message").style.display = "block";
    document.getElementById("messageAlert").innerHTML = message + "<br>";
    refreshJson(response);
}

function alertRun(response) {
    message = response.alertMessage;
    //document.getElementById("overlay-message").style.display = "block";
    //document.getElementById("messageAlert").innerHTML = message + "<br>";
    message = message.replace(/\n/g, "<br>");
    alertMessageLocalSmall(message);
    refreshJson(response);
}

function alertMessageLocal(message) {
    var message = String(message);
    document.getElementById("overlay-message").style.display = "block";
    //document.getElementById("hidden-edit-text-confirm-button").style.display = "none";
    document.getElementById("messageAlert").innerHTML = message + "<br>";
}

function alertMessageLocalSmall(message) {
    var message = String(message);
    document.getElementById("overlay-message").style.display = "block";
    document.getElementById("messageAlert").style.fontSize = "x-large";
    document.getElementById("messageAlert").innerHTML = message;
}

function editTextView(pos) {
    pos = pos.replace(/\D/g,'');  // get only the digit part of position.
    document.getElementById("overlay-input-menu").style.display = "none";
    document.getElementById("overlay-action-edit").style.display = "none";
    document.getElementById("hidden-edit-text-confirm-button").style.display = "inline-block";
    document.getElementById("ConfirmInputButton").style.display = "none";
    document.getElementById("overlay-text").style.display = "block";

    pywebview.api.getTextValue(pos).then(getSetTextActionEdit);
}

function getSetTextActionEdit(response) {
    textFromPos = response.content;
    document.getElementById("textInputField").value = textFromPos;
}

function seqSettingsClick(response) {
    document.getElementById("cpsSpeedField").value = response.jsonSettings.typingSpeed;
    document.getElementById("seqTimeout").value = response.jsonSettings.timeout;
    document.getElementById("overlay-global-seq-settings").style.display = "block";
}
