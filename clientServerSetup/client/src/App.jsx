import { Chess } from 'chess.js';
import { useEffect, useRef, useState } from 'react';
import { Chessboard } from 'react-chessboard';
import { io } from 'socket.io-client';
import './App.css';

function App() {
    const [roomCreated, setRoomCreated] = useState("")
    // Reference for socket of the client
    const socketRef = useRef(null)

    // Stored a given roomID from creating a room
    // Add activeID in case user adds another room
    const [joinID, setJoinID] = useState(null)
    const [activeID, setActiveID] = useState(null)

    // Stores the color client is playing as
    const [gameColor, setColor] = useState(null)

    // Storing whether the game is still in session or not
    const [playing, setGameStatus] = useState(false)
    const [result, setGameResult] = useState(null)

    // Stores local chess instance
    const [chessInstance, setChessInst] = useState(null)
    
    useEffect(() => {
        // set the socket reference to initialize a socket on the specified URL
        socketRef.current = io("https://bse-multichess.onrender.com")
        socketRef.current.on('connect', ()=>{
            console.log("Connection made with server!")
        });

        // Stores the roomID of the server-created room
        socketRef.current.on('roomCreated', (roomID)=>{
            setRoomCreated(roomID)
            setActiveID(roomID)
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
            const newChessInstance = new Chess()
            // should this be the instance or FEN string? 
            setChessInst(newChessInstance)
        })

        // Checking that move made is validated by server
        // If not, undo the move!
        socketRef.current.on('invalidMove', () => {
            setChessInst(prev => {
                const tempInstance = new Chess(prev.fen())
                tempInstance.undo()
                return tempInstance
            })
        })

        // If the other player makes a valid move, we want to update our local state as well
        socketRef.current.on('moveValid', ({fen}) => {
            setChessInst(new Chess(fen))
        })

        // If the game has ended, need to stop play
        socketRef.current.on('gameOver', (winCond) => {
            setGameStatus(false)
            // displaying game over message
            setGameResult(winCond ?? { type: "Game over" })
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

    // For react chess board
    function canDragColorPieces({piece}){
        console.log('piece:', piece, 'gameColor:', gameColor);
        return (piece.pieceType[0] == gameColor);
    }

    function onPieceDrop({sourceSquare, targetSquare}){
        console.log('onPieceDrop fired:', sourceSquare, targetSquare)
        const tempInstance = new Chess(chessInstance.fen())
        try {
            if (playing) {
                // Updates the instance locally
                tempInstance.move({from: sourceSquare, to: targetSquare})
                setChessInst(tempInstance)

                // Need to make the change on the server too
                socketRef.current.emit('makeMove', {roomID:activeID, from:sourceSquare, to:targetSquare})
                return true
            } else {
                console.log("Game ended!")
                return false
            }
        } catch {
            console.log("Invalid move!")
            return false
        }
    }   

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
            onClick={()=>{
                socketRef.current.emit('joinRoom', joinID) 
                setActiveID(joinID)
            }}
        >
            Join room now
        </button>

        {playing ? <p>The game has started!</p> : <p>Game has not started</p>}

        {gameColor ? <p>Playing as {gameColor}</p> : <p></p>}

        {result && (
                <p>
                    {result.winner
                        ? `${result.type}! ${result.winner === 'w' ? 'White' : 'Black'} wins.`
                        : result.type}
                </p>
        )}

        <div style={{ width: '80%' }}>
        {playing && chessInstance && (
            <Chessboard options={{
                canDragPiece: canDragColorPieces,
                onPieceDrop,
                position: chessInstance.fen(),
                boardOrientation: gameColor === 'w' ? 'white' : 'black',
                id: `player-${gameColor}`
            }} />
        )}
        </div>

        </section>
    </>
    )
}

export default App
