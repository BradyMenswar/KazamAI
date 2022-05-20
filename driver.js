const socket = new WebSocket('ws://sim.smogon.com:8000/showdown/websocket');
let challstr;


let username = "barrymcawkner";
let password = "dickdick";
let assertion;

function search(meta) {
    
    socket.send("|/search gen8unratedrandombattle")
    
}



async function login() {
    let fetchURL = 'https://play.pokemonshowdown.com/action.php?act=login&name=' + username + '&pass=' + password + '&challstr=' + challstr;
        console.log(fetchURL);
        assertion = await fetch(fetchURL, {method: "POST"});
        console.log(assertion);

    
    socket.send("|/trn barrymcawkner,0," + assertion);

}

socket.addEventListener('message', function (event) {
    // console.log('Message from server ', event.data);
    if(event.data.includes("challstr"))
    {
        let index = event.data.search(/[0-9]/);
        challstr = event.data.substring(index);
        // challstr = event.data;
        console.log("Challstr: " + challstr);

        
    }
});