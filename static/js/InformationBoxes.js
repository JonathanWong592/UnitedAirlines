// Create X number of buttons depending on the number of kiosks provided

// first test to see if something can be overlayed on the stream
// second: display X number of info buttons on top of the kiosks that are clickable and display the correct information.

// function to get the data from python...

// this remains constant, there will always be 4 info boxes
// Status
// Usage
// Overrides
// Transactions
function showInfoBoxes(clicked_id) {

    // first wipe out all existing boxes if new one is clicked, that way a new box can be created on top of it
    var myobj = document.getElementById("p1");
    if (myobj != null){
        myobj.remove();
    }
    myobj = document.getElementById("p2");
    if (myobj != null){
        myobj.remove();
    }
    myobj = document.getElementById("p3");
    if (myobj != null){
        myobj.remove();
    }
    myobj = document.getElementById("p4");
    if (myobj != null){
        myobj.remove();
    }



    data = [
        {'left': 179.00000274181366, 'top': 315.9999918937683, 'width': 82.01371729373932, 'height': 110.0020158290863, 'status': 'Functional', 'color': 'Green', 'colorCode': '#00FF00', "Reasons": {
            "Status": "",
            "Usage": "",
            "Overrides": "",
            "Transactions": ""
        }},
        {'left': 498.99998903274536, 'top': 320.0000023841858, 'width': 75.99999815225601, 'height': 92.99999713897705, 'status': 'Possibly Functional', 'color': 'Yellow', 'colorCode': '#FFFF00', "Reasons": {
            "1": "User hasn't interacted in 24 hours",
            "Status": "Critical Errors: 4",
            "Usage": "Single Pax: 1,931",
            "Overrides": "Baggage Fee: 114",
            "Transactions": "Count: 9,357"
        }},
        {'left': 825.0000071525574, 'top': 322.99999952316284, 'width': 71.01584494113922, 'height': 97.00915932655334, 'status': 'Non-Functional', 'color': 'Red', 'colorCode': '#FF0000', "Reasons": {
            "1": "UI Broken",
            "Status": "Most Common: Printer 001",
            "Usage": "Multi-Pax: 795",
            "Overrides": "Baggage Exception: 318",
            "Transactions": "Revenue: $41,113"
        }}
    ]

    var p1 = document.createElement('p')
    p1.classList.add("transBox")
    p1.setAttribute("id", "p1")
    p1.type = "p"
    p1.innerHTML = "Status for kiosk " + clicked_id + "<br />" + data[clicked_id - 1]["Reasons"]["Status"]
    p1.style.position = "absolute";
    p1.style.backgroundColor = "gray"
    p1.style.color = "white"
    p1.style.fontSize = "16px"
    p1.style.width =  250 + "px"
    p1.style.height = 130 + "px"
    p1.style.top = 45 + "px"
    p1.style.left = 125 + "px"
    p1.style.opacity = .75
    var container = document.getElementById('vidDisplay')
    container.appendChild(p1)

    var p2 = document.createElement('p')
    p2.classList.add("transBox")
    p2.setAttribute("id", "p2")
    p2.type = "p"
    p2.innerHTML = "Usage for kiosk " + clicked_id + "<br />" + data[clicked_id - 1]["Reasons"]["Usage"]
    p2.style.position = "absolute";
    p2.style.backgroundColor = "gray"
    p2.style.color = "white"
    p2.style.fontSize = "16px"
    p2.style.width =  250 + "px"
    p2.style.height = 130 + "px"
    p2.style.top = 45 + "px"
    p2.style.left = 425 + "px"
    p2.style.opacity = .75
    var container = document.getElementById('vidDisplay')
    container.appendChild(p2)

    var p3 = document.createElement('p')
    p3.classList.add("transBox")
    p3.setAttribute("id", "p3")
    p3.type = "p"
    p3.innerHTML = "Overrides for kiosk " + clicked_id + "<br />" + data[clicked_id - 1]["Reasons"]["Overrides"]
    p3.style.position = "absolute";
    p3.style.backgroundColor = "gray"
    p3.style.color = "white"
    p3.style.fontSize = "16px"
    p3.style.width =  250 + "px"
    p3.style.height = 130 + "px"
    p3.style.top = 45 + "px"
    p3.style.left = 725 + "px"
    p3.style.opacity = .75
    var container = document.getElementById('vidDisplay')
    container.appendChild(p3)

    var p4 = document.createElement('p')
    p4.classList.add("transBox")
    p4.setAttribute("id", "p4")
    p4.type = "p"
    p4.innerHTML = "Transactions for kiosk " + clicked_id + "<br />" + data[clicked_id - 1]["Reasons"]["Transactions"]
    p4.style.position = "absolute";
    p4.style.backgroundColor = "gray"
    p4.style.color = "white"
    p4.style.fontSize = "16px"
    p4.style.width =  250 + "px"
    p4.style.height = 130 + "px"
    p4.style.top = 45 + "px"
    p4.style.left = 1025 + "px"
    p4.style.opacity = .75
    var container = document.getElementById('vidDisplay')
    container.appendChild(p4)

}

function showCoordinates(coordinates){
    return coordinates
}


document.addEventListener('DOMContentLoaded', function load(data) {

    // data = [
    //     {'left': 179.00000274181366, 'top': 315.9999918937683, 'width': 82.01371729373932, 'height': 110.0020158290863, 'status': 'Functional', 'color': 'Green', 'colorCode': '#00FF00', 'Reasons': {}},
    //     {'left': 498.99998903274536, 'top': 320.0000023841858, 'width': 75.99999815225601, 'height': 92.99999713897705, 'status': 'Possibly Functional', 'color': 'Yellow', 'colorCode': '#FFFF00', 'Reasons': {'1': "User hasn't interacted in 24 hours"}},
    //     {'left': 825.0000071525574, 'top': 322.99999952316284, 'width': 71.01584494113922, 'height': 97.00915932655334, 'status': 'Non-Functional', 'color': 'Red', 'colorCode': '#FF0000', 'Reasons': {'1': 'UI Broken'}}
    // ]
    // console.log(data)
    // console.log(typeof data)
    // var data = JSON.parse(data)
    // console.log(data.1)
    // console.log(data)
    numKiosks = 3
    for(i = 1; i < numKiosks + 1; i++){
        // var button = document.createElement('button')
        // // button.setAttribute("id", i)
        // button.classList.add("btn")
        // button.type = 'button'
        // if (Object.keys(data[i-1]['Reasons']).length > 0) {
        //     button.innerHTML = data[i-1]['Reasons']['1']
        // } else { 
        //     button.innerHTML = "Functional"
        // }
        // // change the display coordinates of each
        // button.style.position = "absolute";
        // button.style.backgroundColor = data[i - 1]['colorCode']
        // button.style.color = "white"
        // button.style.fontSize = "16px"

        // // rectangles are being displayed on a 1080x720 image. but the video is being sized up,
        // // so some of the dimensions/coordinates are being messed up.
        // // the video feed is 1280 x 720, so just add 200px to the left (where it starts)

        // // or we can just display the video feed with the same dimensions as the picture taken
        // // setting the button to the correct coordinates
        // button.style.width = parseInt(data[i - 1]['width']) + "px"
        // button.style.height = parseInt(data[i - 1]['height']) + "px"
        // button.style.top = parseInt(data[i - 1]['top']) + "px"
        // button.style.left = parseInt(data[i - 1]['left']) + 200 + "px"


        console.log("BUTONTTNNTNOTN")

        // create info button (above the regular boxes)
        infoButton = document.createElement('button')
        infoButton.setAttribute("id", i)
        infoButton.classList.add("circle")
        infoButton.type='button'
        // edit some of infoButton
        infoButton.style.position = "absolute";
        console.log(data[i])
        console.log(data[i]['colorCode'])
        infoButton.style.backgroundColor = data[i]['colorCode']
        infoButton.style.color = "white"
        infoButton.style.fontSize = "30px"
        infoButton.style.width = 50 + "px"
        infoButton.style.height = 50 + "px"
        infoButton.style.top = parseInt(data[i]['top']) - 100 + "px"
        infoButton.style.left = parseInt(data[i]['left']) + 200 + "px"
        infoButton.innerHTML = "Info"

        // displaying additional information about data
        infoButton.onclick = function () {
            clicked_id = this.id
            var but = document.getElementById(clicked_id)
            if (Object.keys(data[clicked_id]['Reasons']).length > 0) {
                // but.innerHTML = data[i-1]['Reasons']['1']
                // but.innerHTML = "More data from backend"
                // hide info boxes for clickedid

                showInfoBoxes(clicked_id)
                // should instead do non visible to visible?
            } else { 
                but.innerHTML = "Functional"
            }
        }
        
        
        var container = document.getElementById('vidDisplay')
        // container.appendChild(button)
        container.appendChild(infoButton)


        console.log("AFTERBUTTNOTTOTNTONTO")
    }

}, false)

