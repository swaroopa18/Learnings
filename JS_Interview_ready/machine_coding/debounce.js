function debounceT(fn, delay) {
  let timerID;                       // closure state: one timer shared by all calls

  return function (...args) {        // regular function, NOT arrow: we need dynamic `this`
    const context = this;            // capture `this` now; the setTimeout arrow below would keep it too,
                                     // but being explicit is easier to explain in interviews

    clearTimeout(timerID);           // every new call cancels the previous pending call → "reset the timer"

    timerID = setTimeout(() => {
      fn.apply(context, args);       // only the LAST call in a burst reaches here
    }, delay);
  };
}

// leading
const debounce = (fn, delay) => {
  let timerID = null;

  return function (...args) {
    const context = this;

    if (timerID === null) {          // first call of a burst → run immediately
      fn.apply(context, args);
    }

    clearTimeout(timerID);           // FIX: reset the window on EVERY call (this is what makes it debounce)
    timerID = setTimeout(() => {
      timerID = null;                // quiet period ended → next call counts as "first" again
    }, delay);
  };
};

function debounce(fn, delay) {
  let timerID;

  return function (...args) {
    const context = this;
    clearTimeout(timerID);

    return new Promise((resolve, reject) => {
      timerID = setTimeout(async () => {
        try {
          resolve(await fn.apply(context, args));   // works for sync and async fn
        } catch (err) {
          reject(err);
        }
      }, delay);
    });
  };
}

//complete debouce
function debounce(fn, delay, options = {}) {
  const { leading = false, trailing = true } = options;   // lodash-style defaults

  let timerID = null;     // null = no active burst; doubles as "is this the first call?" flag
  let lastArgs;           // args of the most recent call; also means "a trailing call is pending"
  let lastThis;           // `this` of the most recent call
  let result;             // last return value of fn (returned to callers between runs)

  const invoke = () => {
    result = fn.apply(lastThis, lastArgs);
    lastArgs = lastThis = null;   // clear after running → prevents leading+trailing double-fire
                                  // on a single call, because trailing checks `lastArgs`
    return result;
  };

  const debounced = function (...args) {
    const isFirstCall = timerID === null;   // read BEFORE we set a new timer

    lastArgs = args;                        // always remember the latest call
    lastThis = this;

    if (timerID !== null) clearTimeout(timerID);   // reset the quiet period

    if (isFirstCall && leading) invoke();   // leading edge: fire now (this also clears lastArgs)

    timerID = setTimeout(() => {
      timerID = null;                       // burst over
      if (trailing && lastArgs) invoke();   // trailing edge: only if there's an unfired call
    }, delay);

    return result;                          // may be stale/undefined on trailing-only mode
  };

  debounced.cancel = function () {          // e.g. on React component unmount
    clearTimeout(timerID);
    timerID = null;
    lastArgs = lastThis = null;             // drop the pending call entirely
  };

  debounced.flush = function () {           // e.g. save draft before navigating away
    if (timerID === null) return result;    // nothing pending

    clearTimeout(timerID);
    timerID = null;

    if (trailing && lastArgs) return invoke();   // run the pending call immediately

    lastArgs = lastThis = null;
    return result;
  };

  return debounced;
}