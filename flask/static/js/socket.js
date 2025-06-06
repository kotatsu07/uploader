// socket.js
const socket = io();

// 接続時の処理
socket.on('connect', () => {
  console.log('WebSocket接続確立');
});

// 新しいファイル追加イベント
socket.on('new_file_added', (data) => {
  console.log('新しいファイル:', data.filename);
  fetchImageList(); // 他ファイルで定義された関数を呼び出す例
});


