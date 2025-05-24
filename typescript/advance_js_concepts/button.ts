const button = document.querySelector("button")!;

function clickHanlder(message: string) {
  console.log(message);
}
button.addEventListener("click", clickHanlder.bind(null,"swaroopa"));
