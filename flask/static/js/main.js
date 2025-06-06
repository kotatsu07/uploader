document.addEventListener("DOMContentLoaded",() =>{
   const fileInput = document.getElementById('file-input');
  const fileList = document.getElementById('file-list');

  if (!fileInput || !fileList) return;

  fileInput.addEventListener('change', () => {
    fileList.innerHTML = '';

    const files = fileInput.files;
    if (files.length === 0) {
      fileList.innerHTML = '<li>フォルダが選択されていません</li>';
      return;
    }

    // 最初のファイルのwebkitRelativePathからフォルダ名を抽出
    const firstPath = files[0].webkitRelativePath || files[0].name;

    // パス区切りで分割して最初のフォルダ名を取得（例: "myfolder/filename.png" → "myfolder"）
    const folderName = firstPath.split('/')[0];

    const li = document.createElement('li');
    li.textContent = folderName;
    fileList.appendChild(li);
  });

  // fetch('/upload')
  //  .then
    fetchImageList();
   // startImageAutoUpdate();
})