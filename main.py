import asyncio
import websockets
import requests
import json

def hyphenSplit(str):
    if(str.count('-') == 0):
        return str
    elif(str.count('-') == 1):
        return str.split('-')[0]
    return "-".join(str.split('-', 3)[:3])

async def test():
    username = "BarryMcAwkner"
    password = "dickdick"
    
    uri = "ws://sim.smogon.com:8000/showdown/websocket"
    async with websockets.connect(uri) as websocket:

        startMessage = await websocket.recv()
        challstr = await websocket.recv()

        #------------- This is for using an unregistered account. -------------------#

        #ploads1 = {'act': "getassertion", 'userid': username, 'challstr': challstr[8:]}
        #r1 = requests.get("https://play.pokemonshowdown.com/~~showdown/action.php",params=ploads1)
        #print(r1.text)

        ploads2 = {'act': "login", 'name': username, 'pass': password, 'challstr': challstr[10:]}
        head = {'Content-Type': "application/x-www-form-urlencoded; encoding=UTF-8"}

        r2 = requests.post("https://play.pokemonshowdown.com/~~showdown/action.php",headers= head, data=ploads2)
        data = json.loads(r2.text[1:])

        printed = f"|/trn {username},0,{data['assertion']}"
        await websocket.send(printed)

        #------------ Search for battle --------------#
        await websocket.send("|/search gen8unratedrandombattle")

        #------------ Read Server Messages to get battleID -------------#
        battleID = ""
        while(True):
            try:
                test = await asyncio.wait_for(websocket.recv(), timeout= 10)
                if(test[0] == '>'):
                    battleID = hyphenSplit(test[1:])
            except(asyncio.TimeoutError, ConnectionRefusedError):
                test = 'Timeout'
                break
            print(test)

        chooseMove = ""
        while(chooseMove != "1"):
            while(True):
                try:
                    test = await asyncio.wait_for(websocket.recv(), timeout= 3)
                except(asyncio.TimeoutError, ConnectionRefusedError):
                    test = 'Timeout'
                    break
                print(test)
        
            choiceMessage = battleID + "|/choose move 1"
            print(">>SENT MESSAGE:" + choiceMessage )
       
            await websocket.send(choiceMessage)

asyncio.run(test())