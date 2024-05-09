window.addEventListener("load", () => {
  function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); // The maximum is exclusive and the minimum is inclusive
  }
  let infos = [];
  let begin = document.getElementById("begin");

  fetch("media.json").then((r)=>r.json()).then((d) => {
    infos=Array.from(d);
    begin.addEventListener('click', start, {passive: false});
  });

  function start(e) {
    e.preventDefault();
    e.target.innerHTML = "🇵🇸"
    for (let i = 0; i < infos.length; i++) {
      setTimeout(()=>{createWindow(i);}, (i+1) * 5700);
    }
  }

  function createWindow(index) {
    let WW = 480; //getRandomInt(200,500);
    let HH = 240; //getRandomInt(200,500);
    let color = "white";
    const info = infos[index];
    if (info.includes("img")) {
      HH = 480;
      color = "rgb(35, 35, 35)";
    }
    const text = `<!DOCTYPE html><html><head> <title>HCI</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="http://127.0.0.1:5500/index.css"/></head><body><div id="container" data-info=${btoa(info)}></div></body><script>let container = document.getElementById('container'); if (container.dataset.info) container.innerHTML = atob(container.dataset.info); document.body.style.backgroundColor = '${color}';</script></html>`;
    const blob = new Blob([text], {type: "text/html"});
    const blobUrl = URL.createObjectURL(blob);
    window.open(blobUrl, '_blank', `location=0,menubar=0,status=0,scrollbars=0,toolbar=0,resizable=0,popup,width=${WW},height=${HH},left=${getRandomInt(0,screen.width)},top=${getRandomInt(0,screen.height-300)}`);
    window.URL.revokeObjectURL(blobUrl);
  }
});