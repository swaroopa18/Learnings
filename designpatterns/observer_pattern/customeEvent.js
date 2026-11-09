class Ticker extends EventTarget{
  push(value){
    this.dispatchEvent(
      new CustomEvent('tick', {
        detail: value
      })
    )
  }
}

const ticker = new Ticker();

const draw=(tick)=>console.log("draw---",tick.detail)
const play=(tick)=>console.log(tick.detail)

ticker.addEventListener('tick', draw)
ticker.addEventListener('tick', play)

ticker.push('hello')



// -----------------

//abort event
const controller = new AbortController();

const { signal } = controller;

ticker.addEventListener('tick', draw)
ticker.addEventListener('tick', play, {signal})

controller.abort()

ticker.push('hello')