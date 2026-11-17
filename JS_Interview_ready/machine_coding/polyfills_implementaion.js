
// -----------------Promise.all([])
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;

    if (promises.length === 0) {
      resolve(results);
      return;
    }

    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(result => {
          results[index] = result;
          completed++;

          if (completed === promises.length) {
            resolve(results);
          }
        })
        .catch(error => {
          reject(error);
        });
    });
  });
}

// -----------------Promise.allSettled([])
function myPromiseAllSettled(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;
    if (promises.length === 0) {
      resolve([])
      return;
    }
    promises.forEach((p, idx) => {
      Promise.resolve(p).then((result) => {
        results[idx] = { status: 'fulfilled', value: result }
      }).catch((error) => {
        results[idx] = { status: 'rejected', reason: error }
      }).finally(() => {
        completed++;
        if (completed == promises.length) {
          resolve(results)
        }
      })
    })
  });
}

// -----------------Promise.allSettled([])2
function myPromiseAllSettled(promises) {
  return new Promise((resolve, reject) => {
    const results = [];
    let completed = 0;
    if (promises.length === 0) {
      resolve([])
      return;
    }

    promises.forEach((p, idx) => {
      Promise.resolve(p).then(
        result => {
          results[idx] = {
            status: 'fulfilled',
            value: result
          };
        },
        error => {
          results[idx] = {
            status: 'rejected',
            reason: error
          };
        }
      ).finally(() => {
        completed++;

        if (completed === promises.length) {
          resolve(results);
        }
      });

    })
  });
}

// -----------------Promise.race([])
function myPromiseRace(promises) {
  return new Promise((resolve, reject) => {
    if (promises.length === 0) {
      return;
    }
    promises.forEach((p) => {
      Promise.resolve(p).then((result) => {
        resolve(result)
      }).catch((error) => {
        reject(error)
      })
    })
  });
}

const p1 = new Promise(resolve =>
  setTimeout(() => resolve("First"), 3000)
);

const p2 = new Promise((resolve, reject) =>
  setTimeout(() => reject("Second"), 1000)
);

const p3 = new Promise(resolve =>
  setTimeout(() => resolve("Third"), 2000)
);

myPromiseRace([p1, p2, p3])
  .then(console.log)
  .catch(console.error);

// -----------------Promise.any[])

function myPromiseAny(promises) {
  return new Promise((resolve, reject) => {
    if (promises.length == 0) {
      return
    }
    let count = 0
    let errors = []
    promises.forEach((p, idx) => {
      Promise.resolve(p).then((result) => {
        resolve(result)
      }).catch(error => {
        count++;
        errors[idx] = error
        if (count == len(promises)) {
          reject(new AggregateError(errors, "All promises were rejected"));
        }
      })
    })
  });
}

const p11 = Promise.reject("Error 1");
const p22 = new Promise((resolve, reject) =>
  setTimeout(() => reject("Error 2"), 1000)
);
const p33 = new Promise((resolve, reject) =>
  setTimeout(() => reject("Success"), 2000)
);

Promise.any([p11, p22, p33])
  .then(console.log)
  .catch(console.error);