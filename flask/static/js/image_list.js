function fetchImageList() {
    console.log('fetchImageList() が呼ばれました');  
    fetch('/api/image_list')
        .then(response => response.json())
        .then(data => {
            const list = document.getElementById('image-list');
            list.innerHTML = '';
            if (data.length === 0) {
                list.innerHTML = '<li>画像ファイルはありません</li>';
                return;
            }
            data.forEach(filename => {
                const li = document.createElement('li');
                li.textContent = filename;
                list.appendChild(li);
            });
        });
}
window.fetchImageList = fetchImageList;

// function startImageAutoUpdate() {
//     setInterval(fetchImageList, 5000);
// }

document.getElementById('file-input').addEventListener('change', function(event) {
    const files = event.target.files;

    // ステップ①：先に uploads フォルダを空にする
    fetch('/clear_uploads', {
        method: 'POST'
    }).then(() => {
        // ステップ②：空にした後でファイルをアップロード
        const formData = new FormData();
        const allowedTypes = ['image/png', 'image/jpeg', 'image/gif'];

        for (let i = 0; i < files.length; i++) {
            if (allowedTypes.includes(files[i].type)) {
                formData.append('files', files[i]);
            }
        }


            fetch('/upload', {
                method: 'POST',
                body: formData
            }).then(response => {
                if (response.ok) {
                    fetchImageList(); // 成功したらすぐ一覧を更新
                } else {
                    console.error('アップロード失敗');
                }
            });
    });
});