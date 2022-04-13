const express = require('express');
const http = require('http');
const { Server } = require("socket.io");
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/public/index.html');
});

let user_count = 0;
let streaming;

io.on('connection', (socket) => {
  if(user_count === 0) {
    streaming = setInterval(() => {
      const data = fs.readFileSync('../picture/image.jpeg');
      const buffer = Buffer.from(data).toString('base64');
      if(buffer.length > 60e3) {
        socket.broadcast.emit('image', buffer);
      }
    }, 40);
  }

  console.log('User connected');
  user_count++;

  socket.on('disconnect', () => {
    console.log('User disconnected');
    user_count--;
    if(user_count == 0) {
      clearInterval(streaming);
    }
  });
});

server.listen(3000, () => {
  console.log('>>> http://localhost:3000');
});
