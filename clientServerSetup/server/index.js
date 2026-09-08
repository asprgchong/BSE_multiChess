const express = require('express');
const {createServer} = require('node:http');
const {Server} = require('socket.io');
const cors = require('cors');
const crypto = require('crypto');
const {Chess} = require('chess.js');

// Creating a map object to store what chess instance corresponds to each room created
const chessMap = new Map();

// Minimal server that just spins up raw HTTP server (that I pressume can take HTTP requests)
const app = express()
const port = process.env.PORT || 3000;
const server = createServer(app); 

// Attach to socket.io so that the server can listen for websocket events
const io = new Server(server, {cors: {"origin": "https://bse-multichess-frontend.onrender.com"}});

// On the event of connection, we can output that the socket (identified by its ID) is connected to our server
io.on("connection", (socket) => {
    console.log(`${socket.id} connected`);

    // When the socket disconnects, we output that it has disconnected
    socket.on('disconnect', () => {
        console.log("Disconnected"); 
    })

    // When socket sends custom emit event 'createRoom', server makes a
    // unique string of 8 bytes as the roomID. Joins the room and sends to
    // socket the roomID that it has joined to the client
    socket.on('createRoom', () => {
        const roomID = crypto.randomBytes(8).toString('hex');
        socket.join(roomID);
        socket.emit('roomCreated', roomID);
    })

    // When socket sends custom emit event 'joinRoom',
    // server takes a roomID that the socket wants to join.
    // Need to first check if roomID exists and in the case of chess, 
    // If there is < 2 sockets in the room
    socket.on('joinRoom', (roomID) => {
        // Get the map object of roomID and the set of socketIDs of socket attached to room 
        const socketroommap = io.sockets.adapter.rooms;
        if (socketroommap.has(roomID)) {
            // Get the specific set of socketIDs corresponding to the roomID
            // We want to get the room if it exists and check if the room is free to join
            const socketsAttached = socketroommap.get(roomID);
            if (socketsAttached.size == 1){
                socket.join(roomID);
                 // Randomly assign colors to each player
                if (Math.random() < 0.5){
                    console.log(`Assigning: joiner=black, rest-of-room=white`);
                    socket.emit('colorAssign', "b");
                    socket.to(roomID).emit('colorAssign', "w");
                } else {
                    console.log(`Assigning: joiner=white, rest-of-room=black`);
                    socket.emit('colorAssign', "w");
                    socket.to(roomID).emit('colorAssign', "b");
                }

                // Make a chess.js instance when the room has both players
                // Set roomID as key to the corresponding chess instance 
                const chessInstance = new Chess();
                chessMap.set(roomID, chessInstance);

                // Notifies everyone in teh room that the game will begin 
                io.to(roomID).emit('gameStart', "The game will begin!");
            } else {
                socket.emit('roomFull', "This room currently has 2 players already.");
            }
        } else {
            socket.emit('invalidRoom', "Invalid roomID - this room does not exist");
        }
    })


    // **********************************************************************
    // ********* Function for chess implementation and game updates *********
    // **********************************************************************
    socket.on('makeMove', ({roomID, from, to}) => {
        // Check if chess.js instance exists
        if (chessMap.has(roomID)){
            const chessInstance = chessMap.get(roomID);
            // if the game is under play
            if (!chessInstance.isGameOver()){
                // try to make the given move and returns a move object
                // e.g. { color: 'w', from: 'g2', to: 'g3', piece: 'p', san: 'g3' }
                try {
                    const move = chessInstance.move({from: from, to: to});
                    io.to(roomID).emit('moveValid', { fen: chessInstance.fen() });

                    // need to check if mated- if so then end game 
                    if (chessInstance.isGameOver()){
                        const winningCond = {};
                        if (chessInstance.isDrawByFiftyMoves()){
                            winningCond.type = "Draw by Fifty Moves rule";
                        } else if (chessInstance.isInsufficientMaterial()){
                            winningCond.type = "Draw by Insufficient Material";
                        } else if (chessInstance.isThreefoldRepetition()){
                            winningCond.type = "Draw by repetition";
                        } else if (chessInstance.isStalemate()){
                            winningCond.type = "Draw by stalemate";
                        } else {
                            winningCond.winner = chessInstance.turn() == 'b' ? "w" : "b";
                            winningCond.type = "Checkmate";
                        }
                        io.to(roomID).emit('gameOver', winningCond);                        
                    }
                } catch(err) {
                    // otherwise, emit to socket invalid move and does not reflect in server state
                    socket.emit('invalidMove');
                }
            } else {
                // Send a message that game is over.
                io.to(roomID).emit('gameOver'); 
            }
        } else {
            socket.emit('moveError', `No chess instance found`);
        }
    })

});

// Sets the server to listen to a given port and callback just prints that server is set on port and ready to receive emits 
server.listen(port, ()=> {console.log("Server is listening")});

