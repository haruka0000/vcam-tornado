function sendFrame() {
    let cEle = document.createElement('canvas');
    let cCtx = cEle.getContext('2d');
    let vEle = document.getElementById('video');

    cEle.width  = vEle.videoWidth;
    cEle.height = vEle.videoHeight;

    cCtx.drawImage(vEle, 0, 0);  // 動画のフレームを描画

    // Canvasデータを取得
    let canvas_base64 = cEle.toDataURL("image/png");  // DataURI Schema 返却
    
    // form 送信
    const fd = new FormData();
    fd.append("image", canvas_base64);
    axios
        .post('/fakewebcam', fd)
        .then(function (response) {
            console.log("response", response);
        })
        .catch(function (error) {
            console.log(error);
        });
}
setInterval('sendFrame()',0);