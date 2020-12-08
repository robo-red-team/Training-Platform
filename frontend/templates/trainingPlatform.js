// -=== Global variables ===-
let campaignID = ""

// -=== Functions ===-

// Generate a SHA256 hash of key
function GetHashedKey() {
    // Add salt to avoid rainbow table attacks
    let keyPlain = document.getElementById('key').value;
    keyPlain += "RoboRedTeamNotSoSecretSalt"

    // Use forge to generate the SHA256 hash
    let md = forge.md.sha256.create();  
    md.start();  
    md.update(keyPlain, "utf8");  
    return md.digest().toHex();  
} 

// Fill campaign options, based upon data from backend (async request)
function FillCampaignInfo() {
    // Make async request to get the data
    let httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function() {
        // When we get a response, do this:
        if (httpReq.readyState == XMLHttpRequest.DONE) {
            const options = JSON.parse(httpReq.response)
            let optionsHTML = ""

            // Generate HTML options
            for (option in options) { optionsHTML += `<option vlaue="${options[option]}">${options[option]}</option>` }

            // Write it to the document
            document.getElementById("campaignSelect").innerHTML = optionsHTML
        }
    }
    httpReq.open("get", `http://${window.location.hostname}:8855/campaignNames`, true);
    httpReq.send();  
}

// Get campaign info, and show it on the document
function GetCampaignInfo() {
    // Remove old info with loading comment
    document.getElementById("campaignInfo").innerHTML = `<p class="text-center text-light">Loading...</p>`
    document.getElementById("spawnedCampaignInfo").innerHTML = ""

    // Make sure rules are accepted, else tell user to accept the rules
    const ruleAcceptState = document.getElementById("acceptRules").checked
    if (ruleAcceptState) {
        // Get currently selected name
        const campaignName = document.getElementById("campaignSelect").value
        
        // Make async request to get the data
        let httpReq = new XMLHttpRequest();
        httpReq.onreadystatechange = function() {
            // When we get a response, do this:
            if (httpReq.readyState == XMLHttpRequest.DONE) {
                const campaignInfo = JSON.parse(httpReq.response)

                // Add info to HTML, and HTML needed to spawn campaign
                let infoHTML = `<h3 class="text-center text-light">Campaign: ${campaignInfo["name"]}</h3><p class="text-center text-light">${campaignInfo["description"]}</p>`
                infoHTML += `<div class="form-group text-center text-light"><select class="form-control" id="timeWaitMin"><option vlaue="15">15 minutes before attack</option><option vlaue="30">30 minutes before attack</option><option vlaue="45">45 minutes before attack</option><option vlaue="60">60 minutes before attack</option></select><input class="fillWidht" type="text" id="key" placeholder="Key"><button class="btn btn-dark fillWidht text-center text-light" onclick="SpawnCampaign()">Spawn Campaign</button><button class="btn btn-secondary fillWidht text-center text-light" onclick="GetVPNBundle()">Get VPN bundle</button></div>`

                // Write it to the document
                document.getElementById("campaignInfo").innerHTML = infoHTML
            }
        }
        httpReq.open("get", `http://${window.location.hostname}:8855/campaignInfo?name=${campaignName}`, true);
        httpReq.send();
        
    } else {
        document.getElementById("campaignInfo").innerHTML = `<b><p class="text-center text-light">You have to accept the rules, if you wish to use our training platform!</p></b>`
    }
}

// Get a VPN bundle
function GetVPNBundle() {
    // Get key
    const plainKey = document.getElementById("key").value
    const hashedKey = GetHashedKey(plainKey)
    window.open(`http://${window.location.hostname}:8855/vpnBundle?key=${hashedKey}`, "_blank");
}

// Spawn the selected campaign, if the API key is correct
function SpawnCampaign() {
    // Remove old info with loading comment
    document.getElementById("spawnedCampaignInfo").innerHTML = `<p class="text-center text-light">Loading...</p>`

    // Get currently selected name, and hashed key value
    const campaignName = document.getElementById("campaignSelect").value
    const plainKey = document.getElementById("key").value
    const hashedKey = GetHashedKey(plainKey)

    // Set waitTimeMin value, based on selected option
    let waitTimeMin = document.getElementById("timeWaitMin").selectedIndex
    switch(waitTimeMin) {
        case 0:
            waitTimeMin = 15
            break
        case 1:
            waitTimeMin = 30
            break
        case 2: 
            waitTimeMin = 45
            break
        case 3:
            waitTimeMin = 60
            break
    }
    
    // Make async request to get spawn the campaign, and get data
    let httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function() {
        // When we get a response, do this:
        if (httpReq.readyState == XMLHttpRequest.DONE) {
            const campaignInfo = JSON.parse(httpReq.response)
            const spawnedInfo = campaignInfo["machines"]
            campaignID = campaignInfo["id"]
            
            // Make the HTML table to show spawned machine info
            let ids = []
            let ips = []
            let descriptions = []
            let sshpass = []
            for (i = 0; i < spawnedInfo.length; i++) {
                ids.push(spawnedInfo[i]["id"])
                ips.push(spawnedInfo[i]["ip"])
                descriptions.push(spawnedInfo[i]["shortDescription"])
                sshpass.push(spawnedInfo[i]["password"])
            }
            
            let infoHTML = `<b><h2 class="text-center text-light">Spawned Machines:</h2></b><h4 class="text-center text-light">Campaign id: ${campaignID}</h4><p class="text-center text-light">Here is the list of spawned machines, which belong to your campaign.</p><table class="table"><thead><tr><th class="text-light" scope="col">Machine ID</th><th class="text-light" scope="col">Local IP</th><th class="text-light" scope="col">Short description</th><th class="text-light">SSH password</th></tr></thead><tbody>`
            for (i = 0; i < ids.length; i++) {
                infoHTML += `<tr><td class="text-light">${ids[i]}</td><td class="text-light">${ips[i]}</td><td class="text-light">${descriptions[i]}</td><td class="text-light">${sshpass[i]}</td></tr>`
            }
            infoHTML += `</tbody></table>`

            // Write it to the document
            document.getElementById("spawnedCampaignInfo").innerHTML = infoHTML
        }
    }
    document.getElementById('myButton').style.display = ""
    httpReq.open("post", `http://${window.location.hostname}:8855/campaignSpawn?name=${campaignName}&key=${hashedKey}&waitTimeMin=${waitTimeMin}`, true);
    httpReq.send();
}

function SetUpAsyncButton() {
    var myButton = document.querySelector('#myButton');
    myButton.addEventListener('click', GetCampaignResultsAJAX);
}


function GetCampaignResultsAJAX(){
    url = `http://${window.location.hostname}:8855/campaignResults?id=${campaignID}`
    var request = new XMLHttpRequest();
    request.open('GET', url);
    request.addEventListener('readystatechange', handleResponse);
    request.send();
}

function handleResponse() {
    // "this" refers to the object we called addEventListener on
    var request = this;

    /*
    Exit this function unless the AJAX request is complete,
    and the server has responded.
    */
    if (request.readyState != 4)
        return;

    // If there wasn't an error, run our showResponse function
    if (request.status == 200) {
        var ajaxResponse = request.responseText;

        showResponse(ajaxResponse);
    }
}

function showResponse(ajaxResponse) {
    var responseContainer = document.querySelector('#responseContainer');
    jsonResp = JSON.parse(ajaxResponse)
    console.log(ajaxResponse)
    console.log(jsonResp)
    response = "";
    if(ajaxResponse.includes("script not ran yet")){
        response += '<h2 class="text-center text-light">Attacker has not started yet</h2>'
    }else if(ajaxResponse.includes("script running")){
        response +='<h2 class="text-center text-light">Attacker is running, refresh in a few minutes to get results'
    }else{
        response += `<h2 class="text-center text-light">${jsonResp[0]["attackName"]} attack has completed, here are the results</h2>`
        let campaigninfo = jsonResp[0]["checks"];
        let descriptions = [];
        let names = [];
        let patcheds = [];
        let scores = [];
        for (i = 0; i < campaigninfo.length; i++) {
            descriptions.push(campaigninfo[i]["description"]);
            names.push(campaigninfo[i]["name"]);
            patcheds.push(campaigninfo[i]["patched"]);
            scores.push(campaigninfo[i]["score"]);
        }
        response = `<table class="table"><thead><tr><th class="text-light" scope="col">Description</th><th class="text-light" scope="col">Name</th><th class="text-light" scope="col">Patched?</th><th class="text-light">Score</th></tr></thead><tbody>`
            for (i = 0; i < descriptions.length; i++) {
                response += `<tr><td class="text-light">${descriptions[i]}</td><td class="text-light">${names[i]}</td><td class="text-light">${patcheds[i]}</td><td class="text-light">${scores[i]}</td></tr>`;
            }
            response += `</tbody></table>`;

            points = 0;
            total = 0;
            for (i = 0; i < campaigninfo.length; i++) {
                total += scores[i];
                if(patcheds[i]){
                    points += scores[i];
                }
            }
            response += `<h2 class="text-center text-light"> You scored ${points} / ${total}</h2>`
    }

    responseContainer.innerHTML = response;
}


// -=== Initialization ===-
FillCampaignInfo()
SetUpAsyncButton()