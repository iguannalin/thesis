window.addEventListener("load", () => {
  function getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min) + min); // The maximum is exclusive and the minimum is inclusive
  }
  const container = document.getElementById("container");
  let infos = [];
  let interval;
  let index = 0;
  fetch("absence.json").then((r)=>r.json()).then((d)=>
  {
    infos=Array.from(d);
    document.addEventListener('click', start, {passive: false});
  });

  function start(e) {
    e.preventDefault();
    interval = setInterval(createWindow, 5000);
  }

  function createWindow() {
    let sq = getRandomInt(200,500);
    const info = infos[index];
    const text = `<!DOCTYPE html><html> <head> <title>absence</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://iguannalin.github.io/absence/index.css"/></head> <body><div id="overlay"></div> <div id="container" data-info=${btoa(info)}></div></body><script>let container = document.getElementById('container'); if (container.dataset.info) container.innerHTML = atob(container.dataset.info);</script></html>`;
    const blob = new Blob([text], {type: "text/html"});
    const blobUrl = URL.createObjectURL(blob);
    window.open(blobUrl, '_blank', `popup,width=${sq},height=${sq},left=${getRandomInt(300,900)},top=${getRandomInt(100,500)}`);
    window.URL.revokeObjectURL(blobUrl);
    index++;
    console.log({index, infos});
    if (index >= infos.length) 
      clearInterval(interval);
  }
});