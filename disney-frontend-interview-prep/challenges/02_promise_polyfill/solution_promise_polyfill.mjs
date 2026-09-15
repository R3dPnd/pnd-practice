const PENDING = "pending";
const FULFILLED = "fulfilled";
const REJECTED = "rejected";

export class MyPromise {
  #state = PENDING;
  #value;
  #callbacks = [];

  constructor(executor) {
    const resolve = (value) => this.#settle(FULFILLED, value);
    const reject = (reason) => this.#settle(REJECTED, reason);
    try {
      executor(resolve, reject);
    } catch (err) {
      reject(err);
    }
  }

  #settle(state, value) {
    if (this.#state !== PENDING) return;

    // Flatten: if we're "fulfilling" with another thenable, wait on it instead.
    if (state === FULFILLED && value instanceof MyPromise) {
      value.then(
        (v) => this.#settle(FULFILLED, v),
        (e) => this.#settle(REJECTED, e)
      );
      return;
    }

    this.#state = state;
    this.#value = value;
    const callbacks = this.#callbacks;
    this.#callbacks = [];
    queueMicrotask(() => callbacks.forEach((cb) => cb()));
  }

  then(onFulfilled, onRejected) {
    return new MyPromise((resolve, reject) => {
      const handle = () => {
        try {
          if (this.#state === FULFILLED) {
            resolve(typeof onFulfilled === "function" ? onFulfilled(this.#value) : this.#value);
          } else if (typeof onRejected === "function") {
            resolve(onRejected(this.#value));
          } else {
            reject(this.#value);
          }
        } catch (err) {
          reject(err);
        }
      };

      if (this.#state === PENDING) {
        this.#callbacks.push(handle);
      } else {
        queueMicrotask(handle);
      }
    });
  }

  catch(onRejected) {
    return this.then(undefined, onRejected);
  }

  finally(onFinally) {
    return this.then(
      (value) => {
        onFinally();
        return value;
      },
      (reason) => {
        onFinally();
        throw reason;
      }
    );
  }

  static resolve(value) {
    return value instanceof MyPromise ? value : new MyPromise((res) => res(value));
  }

  static reject(reason) {
    return new MyPromise((_res, rej) => rej(reason));
  }

  static all(iterable) {
    return new MyPromise((resolve, reject) => {
      const items = Array.from(iterable);
      if (items.length === 0) {
        resolve([]);
        return;
      }
      const results = new Array(items.length);
      let remaining = items.length;
      items.forEach((item, index) => {
        MyPromise.resolve(item).then((value) => {
          results[index] = value;
          remaining -= 1;
          if (remaining === 0) resolve(results);
        }, reject);
      });
    });
  }
}
