const START = String.fromCharCode(0, 0, 0);
const START_GAME = 110
const WINNER = 104
const LOSER = 104
const TEAM1WIN = 105
const TEAM2WIN = 106
let player1 = -1
let player2 = -1
function start() {
    websocket = new WebSocket("ws://localhost:8888/ws");
    websocket.onopen = function (e) {
        onOpen(e)
    };
    websocket.onclose = function (e) {
        onClose(e)
    };
    websocket.onmessage = function (e) {
        onMessage(e)
    };
    websocket.onerror = function (e) {
        onError(e)
    };
}


function onOpen(e) {
    console.log(e.type);
    let a = 0
    websocket.send(START);

}

function onMessage(e) {
    console.log()
    let p1 = e.data[0].charCodeAt(0)
    let p2 = e.data[1].charCodeAt(0)
    let message = e.data[2].charCodeAt(0)
    player1 = p1
    player2 = p2
    console.log(p1, p2, message);

    if (message === START_GAME) {
        document.getElementById('0').disabled = false;
        document.getElementById('1').disabled = false;
        document.getElementById('2').disabled = false;
        document.getElementById('3').disabled = false;
    } else if (message === WINNER) {
        document.getElementById('0').disabled = true;
        document.getElementById('1').disabled = true;
        document.getElementById('2').disabled = true;
        document.getElementById('3').disabled = true;
        draw_heart(ctx, 20,40);
    } else if (message === TEAM1WIN) {
        draw_team1victory(ctx, 30, 80);
    } else if (message === TEAM2WIN) {
        draw_team2victory(ctx, 30, 80); 
    } else if (message === LOSER) {
        document.getElementById('0').disabled = true;
        document.getElementById('1').disabled = true;
        document.getElementById('2').disabled = true;
        document.getElementById('3').disabled = true;
    }
}

function onError(e) {
    console.log('rcvd: ' + e.data);
    websocket.close();
}

function onClose(e) {
    websocket.close();
}


function onClick1(){
    let n = 1
    websocket.send(String.fromCharCode(player1, player2, n))
}

function onClick2(){
    let n = 2
    websocket.send(String.fromCharCode(player1, player2, n))
}

function onClick3(){
    let n = 3
    websocket.send(String.fromCharCode(player1, player2, n))
}


function onClick4(){
    let n = Math.random()*3+1
    websocket.send(String.fromCharCode(player1, player2, n))
}

window.addEventListener("load", start, false);


var canvas = document.getElementById('c');
var ctx = canvas.getContext('2d');

function draw_heart(ctx1, pos_x, pos_y){
    ctx1.fillStyle = "red";
    
    ctx1.beginPath();
    ctx1.arc(pos_x+98,pos_y+30,30,0,2*Math.PI);
    
    ctx1.fill();
    
    ctx1.beginPath();
    ctx1.arc(pos_x+152,pos_y+30,30,0,2*Math.PI);
    ctx1.fill();
    
    ctx1.beginPath();
    ctx1.moveTo(pos_x+70, pos_y+44); 
    ctx1.lineTo(pos_x+125, pos_y+110);
    ctx1.lineTo(pos_x+180, pos_y+43);
    ctx1.fill();
    
}

function draw_bheart(ctx1, pos_x, pos_y){
    ctx1.fillStyle = "black";
    
    ctx1.beginPath();
    ctx1.arc(pos_x+98,pos_y+30,30,0,2*Math.PI);
    
    ctx1.fill();
    
    ctx1.beginPath();
    ctx1.arc(pos_x+152,pos_y+30,30,0,2*Math.PI);
    ctx1.fill();
    
    ctx1.beginPath();
    ctx1.moveTo(pos_x+70, pos_y+44); 
    ctx1.lineTo(pos_x+125, pos_y+110);
    ctx1.lineTo(pos_x+180, pos_y+43);
    ctx1.fill();
    
}

function draw_team1victory(ctx1, pos_x, pos_y){
    ctx.fillStyle = 'blue';
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(100,50);
    ctx.lineTo(50, 100);
    ctx.lineTo(0, 90);
    ctx.closePath();
    ctx.fill();
}

function draw_team2victory(ctx1, pos_x, pos_y){
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(100,50);
    ctx.lineTo(50, 100);
    ctx.lineTo(0, 90);
    ctx.closePath();
    ctx.fill();
}