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
    httpReq.open("get", `http://localhost:8855/campaignNames`, true);
    httpReq.send();  
}

// Get campaign info, and show it on the document
function GetCampaignInfo() {
    // Get currently selected name
    campaignName = document.getElementById("campaignSelect").value
    
    // Make async request to get the data
    let httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function() {
        // When we get a response, do this:
        if (httpReq.readyState == XMLHttpRequest.DONE) {
            const campaignInfo = JSON.parse(httpReq.response)

            // Add info to HTML, and HTML needed to spawn campaign
            let infoHTML = `<h3 class="text-center">Campaign: ${campaignInfo["name"]}</h3><p class="text-center">${campaignInfo["description"]}</p>`
            infoHTML += `<div class="form-group text-center"><input type="text" id="key" placeholder="Key"><button class="btn btn-secondary text-center" onclick="SpawnCampaign()">Spawn Campaign</button></div>`

            // Write it to the document
            document.getElementById("campaignInfo").innerHTML = infoHTML
        }
    }
    httpReq.open("get", `http://localhost:8855/campaignInfo?name=${campaignName}`, true);
    httpReq.send();
}

// Spawn the selected campaign, if the API key is correct
function SpawnCampaign() {
    // Get currently selected name, and hashed key value
    campaignName = document.getElementById("campaignSelect").value
    plainKey = document.getElementById("key").value
    hashedKey = GetHashedKey(plainKey)
    
    // Make async request to get spawn the campaign, and get data
    let httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function() {
        // When we get a response, do this:
        if (httpReq.readyState == XMLHttpRequest.DONE) {
            const spawnedInfo = JSON.parse(httpReq.response)
            
            // Make the HTML table to show spawned machine info
            ids = []
            ips = []
            for (i = 0; i < spawnedInfo.length; i++) {
                ids.push(spawnedInfo[i]["id"])
                ips.push(spawnedInfo[i]["ip"])
            }
            let infoHTML = `<b><h2 class="text-center">Spawned Machines:</h2></b><p class="text-center">Here is the list of spawned machines, which belong to your campaign.</p><table class="table"><thead><tr><th scope="col">Machine ID</th><th scope="col">Local IP</th></tr></thead><tbody>`
            for (i = 0; i < ids.length; i++) {
                infoHTML += `<tr><td>${ids[i]}</td><td>${ips[i]}</td></tr>`
            }
            infoHTML += `</tbody></table>`

            // Write it to the document
            document.getElementById("spawnedCampaignInfo").innerHTML = infoHTML
        }
    }
    httpReq.open("post", `http://localhost:8855/campaignSpawn?name=${campaignName}&key=${hashedKey}`, true);
    httpReq.send();
}

// -=== Initialization ===-
FillCampaignInfo()