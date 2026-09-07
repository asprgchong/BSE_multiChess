import { useEffect, useRef, useState } from 'react';
import { io } from 'socket.io-client';
import './App.css';

function App() {
    const [roomCreated, setRoomCreated] = useState("")
    // Reference for socket of the client
    const socketRef = useRef(null)
    // Stored a given roomID from creating a room
    const [joinID, setJoinID] = useState(null)
    // Stores the color client is playing as
    const [gameColor, setColor] = useState(null)
    // Storing whether the game is still in session or not
    const [playing, setGameStatus] = useState(false)

    useEffect(() => {
        // set the socket reference to initialize a socket on the specified URL
        socketRef.current = io("http://localhost:3000")
        socketRef.current.on('connect', ()=>{
            console.log("Connection made with server!")
        });

        // Stores the roomID of the server-created room
        socketRef.current.on('roomCreated', (roomID)=>{
            setRoomCreated(roomID)
        })

        // Stores the colorAssigned by the server for the game
        socketRef.current.on('colorAssign', (color)=> {
            console.log(`Playing as ${color}`)
            setColor(color)
        })

        // Stores if the game has started or not
        socketRef.current.on('gameStart', (message) => {
            console.log(message)
            setGameStatus(true)

            // If the game has started, we will create a chess.js instance as
            // our local instance.
        })

        // If roomID passed to server is invalid or room to join is full, output
        socketRef.current.on('invalidRoom', (message) => {
            console.log(message)
        })

        socketRef.current.on('roomFull', (message) => {
            console.log(message)
        })

        return () => {
            socketRef.current.disconnect()
            console.log("Disconnected")
        }
    }, [])

    return (
    <>
        <section id="center">
        <button
            type="button"
            className="makeRoom"
            onClick={() => {socketRef.current.emit('createRoom')}}
        >
            Create Room
        </button>

        {roomCreated ? <p>Room created: {roomCreated}</p> : <p>Room not created</p>}

        <input type='text' name='roomID' onChange={(e)=>setJoinID(e.target.value)} />

        {/* Button used to join a room via a given roomID. Emit to server with ID to join. */}
        <button
            type="button"
            className="joinRoom"
            onClick={()=>{socketRef.current.emit('joinRoom', joinID)}}
        >
            Join room now
        </button>

        {playing ? <p>The game has started!</p> : <p>Game has not started</p>}

        {gameColor ? <p>Playing as {gameColor}</p> : <p></p>}

        </section>
    </>
    )
}

export default App
