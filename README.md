# BSE_multiChess
This is my multiplayer chess project for learning and implementing everything I need to build a collaborative chess puzzle solver to solve puzzles with my friends. I am building this to be able to talk through puzzle ideas and collaboratively learn puzzle patterns, learn about game development / working with servers and clients, and having fun learning by doing. 

## File Structure
```
├── clientServerSetup/
│   ├── client/
│   └── server/
├── local_dev/
├── tests/
└── web/
```

1. ```local_dev```
To implement the basics of Chess, I started with Python and using its OOP functionality and used pygame to run the game loop and user interaction mechanisms. I used a Class for a Piece, then each type of piece which inherited the Piece class, a Board class for keeping track of the game state, and a Tile class for checking the coordinate square. To start implementing the puzzle solving feature, I call chess.com API to get the daily puzzle set up and process the FEN to be reflected on the board for the user to solve. Mimicking chess.com functionality, the puzzle automoves for the opponent until the puzzle is solved. ```tests``` is a work in progress for learning how to write tests in Python to simulate unit tests for my chess implementation and deterministically demonstrate confidence in the code. 

2. ```web```
In an attempt to bring my python chess start onto the web, I learned about Pygbag which took the pygame instance that I had and packaged it into WebAssembly which was compatible to run on a web browser. This [quick start](https://pygame-web.github.io/wiki/pygbag/) made it really easy and quick to transform the pygame folder into a ready to host web game

3. ```clientServerSetup```
Implements a basic Express app that attaches socket.io to an HTTP server for game event response and handling. I use ```chess.js``` and ```react-chessboard``` to implement the game rules, checks, and rendering the board. I render the frontend with React (Vite) which can be found in ```client/``` and the backend is Node found in ```server/```. This is what I actually needed to bring my ideas reliably onto a web environment. 

## Development / Testing
To test the Python implementation: 
1. Navigate to ```local_dev/``` 
2. Run ```pip install -r requirements.txt```
3. Run ```python gameLogic.py``` to start the pygame instance

To run the pytests: 
1. Navigate to ```tests/```
2. Run ```python test_pawns.py```
(for now)

To run / test the Express app version:
1. Navigate to ```clientServerSetup/```
2. Open up 2 terminals and navigate to ```client/``` and ```server/``` in each respectively
3. Run ```npm run dev``` in the client folder 
4. Run ``` node index.js``` in the server folder 
5. Open 2 tabs of localhost:5173 in your browser to simulate the multiplayer game

## Production / Hosting
The client server setup is currently hosted on Render's free tier with the backend as a web service and the frontend as a static website. Render allows users to integrate a specific github repo so that upon commits / upon passing CI, your services are automatically rebuilt and deployed. 

To ensure that the client/frontend and server/backend parts are communicating, ensure that you change: 
1. In ```clientServerSetup/client/src/App.jsx```, change the URL of your backend to the socket reference link: ```socketRef.current = io(<insertURL>)```
2. In ```clientServerSetup/server/index.js```, change the CORS setting to include your frontend URL to avoid origin resource sharing errors: ```{cors: {"origin": "<insertURL>"}}```

## Demo of my server and client!
https://github.com/user-attachments/assets/37d60f76-49d6-47b1-9bcc-aec28ef27175
