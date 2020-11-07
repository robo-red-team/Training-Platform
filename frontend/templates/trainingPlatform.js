// -=== Functions ===-

// Spawn a machine on the host system
function SpawnMachine() {
    let httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function() {
        if (httpReq.readyState == XMLHttpRequest.DONE) {
            document.getElementById("TextOutput").innerHTML = httpReq.response;
        }
    }
    httpReq.open("post", `http://localhost:8855/spawnMachine?key=${GetHashedKey()}&machineName=${document.getElementById("machineName").value}`, true);
    httpReq.send();
}

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
    // When we get a response, do this:
    httpReq.onreadystatechange = function() {
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

// -=== Initialization ===-
FillCampaignInfo()