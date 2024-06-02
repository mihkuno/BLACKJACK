import clustering from 'density-clustering';

var deck_cards = [
    '10C', '10D', '10H', '10S', '2C', '2D', '2H', '2S', '3C', '3D', 
    '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C', 
    '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S', 
    '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 
    'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS'
];
var omega_value = {
    '10C': -2, '10D': -2, '10H': -2, '10S': -2,
    '2C': 1, '2D': 1, '2H': 1, '2S': 1,
    '3C': 1, '3D': 1, '3H': 1, '3S': 1,
    '4C': 2, '4D': 2, '4H': 2, '4S': 2,
    '5C': 2, '5D': 2, '5H': 2, '5S': 2,
    '6C': 2, '6D': 2, '6H': 2, '6S': 2,
    '7C': 1, '7D': 1, '7H': 1, '7S': 1,
    '8C': 0, '8D': 0, '8H': 0, '8S': 0,
    '9C': -1, '9D': -1, '9H': -1, '9S': -1,
    'AC': -2, 'AD': -2, 'AH': -2, 'AS': -2,
    'JC': -2, 'JD': -2, 'JH': -2, 'JS': -2,
    'KC': -2, 'KD': -2, 'KH': -2, 'KS': -2,
    'QC': -2, 'QD': -2, 'QH': -2, 'QS': -2
}

var basic_strategy = [
// D  2   3   4   5   6   7   8   9  10   A             P

    // Hard Totals
    ['H','H','H','H','H','H','H','H','H','H'], //       0
    ['H','H','H','H','H','H','H','H','H','H'], //       1
    ['H','H','H','H','H','H','H','H','H','H'], //       2
    ['H','H','H','H','H','H','H','H','H','H'], //       3
    ['H','H','H','H','H','H','H','H','H','H'], //       4
    ['H','H','H','H','H','H','H','H','H','H'], //       5
    ['H','H','H','H','H','H','H','H','H','H'], //       6
    ['H','H','H','H','H','H','H','H','H','H'], //       7
    ['H','H','H','H','H','H','H','H','H','H'], //       8
    ['H','D','D','D','D','H','H','H','H','H'], //       9
    ['D','D','D','D','D','D','D','D','H','H'], //       10
    ['D','D','D','D','D','D','D','D','D','D'], //       11
    ['H','H','S','S','S','H','H','H','H','H'], //       12
    ['S','S','S','S','S','H','H','H','H','H'], //       13
    ['S','S','S','S','S','H','H','H','H','H'], //       14
    ['S','S','S','S','S','H','H','H','Z','H'], //       15
    ['S','S','S','S','S','H','H','Z','Z','Z'], //       16
    ['S','S','S','S','S','S','S','S','S','S'], //       17
    ['S','S','S','S','S','S','S','S','S','S'], //       18
    ['S','S','S','S','S','S','S','S','S','S'], //       19
    ['S','S','S','S','S','S','S','S','S','S'], //       20

    // Soft Totals
    ['H','H','H','D','D','H','H','H','H','H'], // A,2   21
    ['H','H','H','D','D','H','H','H','H','H'], // A,3   22
    ['H','H','D','D','D','H','H','H','H','H'], // A,4   23
    ['H','H','D','D','D','H','H','H','H','H'], // A,5   24
    ['H','D','D','D','D','H','H','H','H','H'], // A,6   25
    ['d','d','d','d','d','S','S','H','H','H'], // A,7   26
    ['S','S','S','S','d','S','S','S','S','S'], // A,8   27
    ['S','S','S','S','S','S','S','S','S','S'], // A,9   28

    // Pairs
    ['y','y','Y','Y','Y','Y','H','H','H','H'], // 2,2   29
    ['Y','Y','Y','Y','Y','Y','H','H','H','H'], // 3,3   30
    ['H','H','H','y','y','H','H','H','H','H'], // 4,4   31
    ['D','D','D','D','D','D','D','D','H','H'], // 5,5   32
    ['y','Y','Y','Y','Y','H','H','H','H','H'], // 6,6   33
    ['Y','Y','Y','Y','Y','Y','H','H','H','H'], // 7,7   34
    ['Y','Y','Y','Y','Y','Y','Y','Y','Y','Y'], // 8,8   35
    ['Y','Y','Y','Y','Y','S','Y','Y','S','S'], // 9,9   36
    ['S','S','S','S','S','S','S','S','S','S'], // 10,10 37
    ['Y','Y','Y','Y','Y','Y','Y','Y','Y','Y']  // A,A   38
];

var strategy_description = {
    'H': 'Hit',
    'S': 'Stand',
    'D': 'Double if possible, otherwise Stand',
    'd': 'Double if possible, otherwise Hit',
    'Y': 'Split',
    'y': 'Split if Double After Split is allowed', 
    'Z': 'Surrender or Hit if Surrender is not allowed'
}

function getCardValue(card) {
    let value = card.slice(0, -1);

    if (value == 'A') {
        return 11;
    }
    else if (value == 'J' || value == 'Q' || value == 'K') {
        return 10;
    }
    else {
        return parseInt(value);
    }
}


function getStrategy(count, cards, dealerFaceCard=null) {
        

    // check if player has a blackjack or bust
    if (count >= 21) return;
    
    // check if dealer is null
    else if (dealerFaceCard == null) {
        return 'Waiting for next round..';
    }
    
    // row index of the basic strategy table
    const dealerIndex = getCardValue(dealerFaceCard) - 2;

    // used on pairs and soft hands
    const isTwoCard = cards.length == 2;
    const card1 = getCardValue(cards[0]);
    const card2 = getCardValue(cards[1]);

    // check if player has a pair
    if (isTwoCard && (card1 == card2) ) {
        return strategy_description[basic_strategy[29 + card1 - 2][dealerIndex]];
    }

    // check if player has a soft hand
    else if (isTwoCard && (card1 == 11 || card2 == 11)) {
        // Identify the value of the non-Ace card
        const nonAceCard = (card1 == 11) ? card2 : card1;
        return strategy_description[basic_strategy[21 + nonAceCard - 2][dealerIndex]];
    }

    // check if player has a hard hand
    else {
        return strategy_description[basic_strategy[count][dealerIndex]];
    }
}


var deck_count   = window.prompt("How many decks of cards do you want to use? \n(Enter a number between 1 to 10)");

// var deck_count = 1;

for (let i = 0; i < deck_count-1; i++) {
    deck_cards = deck_cards.concat(deck_cards);
}

const container = document.getElementById('grid-container');

deck_cards.forEach(str => {
    const item = document.createElement('div');
    item.className = 'grid-item-remaining';
    item.textContent = str;
    item.detectId = -1;
    container.appendChild(item);
});

// get video dom element
var stream = document.getElementById('stream');




// request access to webcam
// navigator.mediaDevices.getUserMedia({video: {width: stream.offsetWidth, height: stream.offsetHeight }}).then((frame) => stream.srcObject = frame);


// get video dom element
// var stream = document.getElementById('stream');
var videoSelect = document.getElementById('videoSource');

function getConnectedDevices(type, callback) {
    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            const filtered = devices.filter(device => device.kind === type);
            callback(filtered);
        });
}


function startStream(deviceId) {
    if (window.stream && window.stream.getTracks) {
        window.stream.getTracks().forEach(track => track.stop());
    }
    const constraints = {
        video: {
            deviceId: deviceId ? { exact: deviceId } : undefined,
            width: stream.offsetWidth,
            height: stream.offsetHeight
            
        }
    };
    navigator.mediaDevices.getUserMedia(constraints)
        .then((frame) => {
            stream.srcObject = frame;
            window.stream = frame; // Assign the MediaStream object to window.stream
        })
        .catch((error) => {
            console.error('Error accessing media devices.', error);
        });
}


function gotDevices(deviceInfos) {
    videoSelect.innerHTML = '';
    deviceInfos.forEach(deviceInfo => {
        const option = document.createElement('option');
        option.value = deviceInfo.deviceId;
        option.text = deviceInfo.label || `Camera ${videoSelect.length + 1}`;
        videoSelect.appendChild(option);
    });
    videoSelect.onchange = () => startStream(videoSelect.value);
}

function initializeCamera() {
    navigator.mediaDevices.enumerateDevices()
        .then(devices => {
            const videoDevices = devices.filter(device => device.kind === 'videoinput');
            if (videoDevices.length > 0) {
                startStream(videoDevices[0].deviceId);
            }
        });
}

getConnectedDevices('videoinput', gotDevices);
initializeCamera(); // Initialize camera with the first available device

// Other parts of your code...



// request access to webcam
// navigator.mediaDevices.getUserMedia({video: {width: stream.offsetWidth, height: stream.offsetHeight }}).then((frame) => stream.srcObject = frame);



// returns a frame encoded in base64
const getFrame = () => {
    const canvas = document.createElement('canvas');
    canvas.width = stream.offsetWidth;
    canvas.height = stream.offsetHeight;
    canvas.getContext('2d').drawImage(stream, 0, 0);
    const data = canvas.toDataURL('image/png');
    return data;
}

// Change this if you serve on different server or port
// const WS_URL = 'ws://localhost:8000/ws'
const WS_URL = 'wss://2217o5b2zh9g6g-8000.proxy.runpod.net/ws'; 

const ws = new WebSocket(WS_URL);

const dbscan = new clustering.DBSCAN();

ws.onopen = () => {
    console.log(`Connected to ${WS_URL}`);
    
    ws.send(getFrame());
}

ws.onmessage = message => {

    const detection_container = document.getElementById('detection-container');
    // Select all div elements within the parent div
    var divsToRemove = detection_container.querySelectorAll("div");
    // Iterate over the div elements and remove them
    divsToRemove.forEach(function(div) {
        div.remove();
    });

    const detections = JSON.parse(message.data);
    let coordinates = [];

    detections.forEach((detection) => {
        const [x1, y1, x2, y2, name, score, id] = detection;

        coordinates.push([x1, y1]);

        // handling the output bounding boxes                
        // create a div element
        var div = document.createElement('div');
        
        // set div style
        div.style.position = 'absolute';
        div.style.left = `${x1}px`;
        div.style.top = `${y1}px`;
        div.style.width = `${x2 - x1}px`;
        div.style.height = `${y2 - y1}px`;
        div.style.border = '4px solid #a29bfe';
        div.style.color = 'black';
        div.style.display = 'flex';
        div.style.justifyContent = 'center';
        div.style.alignItems = 'center';
        div.style.textAlign = 'center';
        div.style.fontSize = '20px';
        div.style.fontWeight = 'bold';
        div.style.fontFamily = 'arial';
        div.style.backgroundColor = 'rgba(162,155,254, 0.4)';
        div.innerHTML = `${name} <br> ${score * 100}% <br> ${id}`;

        // append div to detection_container
        detection_container.appendChild(div);


        // handling the count of cards                
        for (let item of container.childNodes) {
            if (item.textContent == name && item.detectId == id) {
                break;
            }
            else if (item.textContent == name && item.detectId == -1) {
                item.detectId = id;
                item.className = 'grid-item-tracked';

                const running_count = document.getElementById('running-count-text');
                const running_value = parseInt(running_count.textContent.split(' : ')[1]) + parseInt(omega_value[name]);
                running_count.textContent = 'Running Count : ' + running_value.toString();
                break;
            }   
        }
    });

    // start checking for player and dealer clusters if there are at least 3 detections
    if (detections.length < 3) {
        setTimeout(() => { ws.send(getFrame()); }, 1);
        return;
    }

    var clusters = dbscan.run(coordinates, 500, 2);
    console.log(clusters, dbscan.noise);

    
    let dealerFaceCard = null;

    // check if there is one dealer face card up detected (noise)
    if (dbscan.noise.length >= 1) {


        // find the noise that has the minimum y value
        let miny = Infinity;
        let bucket = [];
        dbscan.noise.forEach(noise_point => {
            const [x1, y1, x2, y2, card, score, id] = detections[noise_point];

            if (y1 < miny) {
                miny = y1;
                dealerFaceCard = card;
                bucket = detections[noise_point];
            }
        });
        const [x1, y1, x2, y2, card, score, id] = bucket;


        // create a div element
        var div = document.createElement('div');
        
        // set div style
        div.style.position = 'absolute';
        div.style.left = `${x1-40}px`;
        div.style.top = `${y1-40}px`;
        div.style.width = `${x2 - x1 + 40}px`;
        div.style.height = `${y2 - y1 + 40}px`;
        div.style.border = '4px solid #a29bfe';
        div.style.color = 'black';
        div.style.fontSize = '20px';
        div.style.fontWeight = 'bold';
        div.style.fontFamily = 'arial';
        div.style.backgroundColor = 'rgba(162,155,254, 0.2)';
        div.style.zIndex = 1;
        div.style.padding = '10px';
        div.style.borderRadius = '20px';
        div.innerHTML = `Dealer's Card`;

        // append div to detection_container
        detection_container.appendChild(div);
    }


    // if no dealer face card, find the dealer's cluster that contains the cluster point minimum y value
    let dealerClusterIndex = null;   
    let dealerClusterCount = 0;

    if (dealerFaceCard == null) {
        let miny = Infinity; 

        clusters.forEach((cluster, index) => {
            cluster.forEach(cluster_point => {
                const [x1, y1, x2, y2, card, score, id] = detections[cluster_point];
                if (y1 < miny) {
                    miny = y1;
                    dealerClusterIndex = index;
                }

                let numberOfAceDetected = 0;
                if (getCardValue(card) == 11) {
                    numberOfAceDetected += 1;
                }
    
                dealerClusterCount += getCardValue(card);
                
                while (dealerClusterCount > 21 && numberOfAceDetected > 0) {
                    dealerClusterCount -= 10;
                    numberOfAceDetected -= 1;
                }
                
            });
        });
    }


    clusters.forEach((cluster, index) => {
        
        let minx = Infinity;
        let miny = Infinity;
        let maxx = -Infinity;
        let maxy = -Infinity;

        let count = 0;
        let cards = [];

        let numberOfAceDetected = 0;
        cluster.forEach(cluster_point => {
            const [x1, y1, x2, y2, card, score, id] = detections[cluster_point];
            if (x1 < minx) minx = x1;
            if (y1 < miny) miny = y1;
            if (x2 > maxx) maxx = x2;
            if (y2 > maxy) maxy = y2;
            
            if (getCardValue(card) == 11) {
                numberOfAceDetected += 1;
            }

            count += getCardValue(card);
            cards.push(card);
        });

        while (count > 21 && numberOfAceDetected > 0) {
            count -= 10;
            numberOfAceDetected -= 1;
        }


        // handling the output bounding boxes for clusters                
        // create a div element
        var div = document.createElement('div');
        // set div style
        div.style.position = 'absolute';
        div.style.left = `${minx-40}px`;
        div.style.top = `${miny-40}px`;
        div.style.width = `${maxx - minx + 40}px`;
        div.style.height = `${maxy - miny + 40}px`;
        div.style.border = '4px solid #a29bfe';
        div.style.color = 'black';
        div.style.fontSize = '20px';
        div.style.fontWeight = 'bold';
        div.style.fontFamily = 'arial';
        div.style.zIndex = 1;
        div.style.padding = '10px';
        div.style.borderRadius = '20px';


        const strategy = getStrategy(count, cards, dealerFaceCard); 

        if (dealerFaceCard == null && dealerClusterIndex == index) {
            div.style.border = '4px solid rgba(255,165,0, 1)';

            if (count == 21) {
                div.style.backgroundColor = 'rgba(0,208,98, 0.6)';
                div.innerHTML = `Dealer: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> BLACKJACK`;
            }
            else if (count > 21) {
                div.style.backgroundColor = 'rgba(255,99,71, 0.6)';
                div.innerHTML = `Dealer: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> BUST`;
            }
            else {
                div.style.backgroundColor = 'rgba(255,165,0, 0.6)';
                div.innerHTML = `Dealer: ${index} <br> Count: ${count} <br> Cards: [${cards}]`;
            }

        }
        else if (dealerFaceCard == null) {            
            if (count == 21) {
                div.style.backgroundColor = 'rgba(0,208,98, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> BLACKJACK`;
            }
            else if (count > 21) {
                div.style.backgroundColor = 'rgba(255,99,71, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> BUST`;
            }
            else if (count > dealerClusterCount) {
                div.style.backgroundColor = 'rgba(0,208,98, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> WINNER`;
            }
            else if (count < dealerClusterCount) {
                div.style.backgroundColor = 'rgba(255,99,71, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> LOSER`;
            }
            else if (count == dealerClusterCount) {
                div.style.backgroundColor = 'rgba(255,165,0, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> TIE`;
            }
        }
        else {       
            if (count == 21) {
                div.style.backgroundColor = 'rgba(0,208,98, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> BLACKJACK`;
            }
            else if (count > 21) {
                div.style.backgroundColor = 'rgba(255,99,71, 0.6)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> BUST`;
            }
            else {
                div.style.backgroundColor = 'rgba(162,155,254, 0.2)';
                div.innerHTML = `Player: ${index} <br> Count: ${count} <br> Cards: [${cards}] <br> Strategy: ${strategy}`;
            }
        }


        // append div to detection_container
        detection_container.appendChild(div);
    });

    setTimeout(() => { ws.send(getFrame()); }, 1);
}