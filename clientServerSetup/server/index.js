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
const io = new Server(server, {cors: {"origin": "*"}});

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
                    socket.emit('colorAssign', "black");
                    socket.to(roomID).emit('colorAssign', "white");
                } else {
                    socket.emit('colorAssign', "white");
                    socket.to(roomID).emit('colorAssign', "black");
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

});

// Sets the server to listen to a given port and callback just prints that server is set on port and ready to receive emits 
server.listen(port, ()=> {console.log("Server is listening")});
