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

  fetch("media.json").then((r)=>r.json()).then((d) => {
    infos=Array.from(d);
    document.addEventListener('click', start, {passive: false});
  });

  function start(e) {
    e.preventDefault();
    if (index == 0) createWindow();
  }

  function createWindow() {
    let sq = getRandomInt(200,500);
    const info = infos[index];
    const text = `<!DOCTYPE html><html> <head> <title>absence</title> <meta charset="utf-8"> <meta name="viewport" content="width=device-width, initial-scale=1"> <link rel="stylesheet" href="https://iguannalin.github.io/thesis/presentation/index.css"/></head> <body><div id="overlay"></div> <div id="container" data-info=${btoa(info)}></div></body><script>let container = document.getElementById('container'); if (container.dataset.info) container.innerHTML = atob(container.dataset.info);</script></html>`;
    const blob = new Blob([text], {type: "text/html"});
    const blobUrl = URL.createObjectURL(blob);
    window.open(blobUrl, '_blank', `location=0,menubar=0,status=0,scrollbars=0,toolbar=0,resizable=0,popup,width=${sq},height=${sq},left=${getRandomInt(0,screen.width)},top=${getRandomInt(0,screen.height)}`);
    window.URL.revokeObjectURL(blobUrl);
    index++;
    if (index == 1) interval = setInterval(createWindow, 20);
    console.log({index, infos});
    if (index >= infos.length) 
      clearInterval(interval);
  }
});