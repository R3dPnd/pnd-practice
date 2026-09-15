export class EventEmitter {
  #listeners = new Map();

  on(event, handler) {
    if (!this.#listeners.has(event)) this.#listeners.set(event, new Set());
    this.#listeners.get(event).add(handler);
    return this;
  }

  off(event, handler) {
    this.#listeners.get(event)?.delete(handler);
    return this;
  }

  once(event, handler) {
    const wrapper = (...args) => {
      this.off(event, wrapper);
      handler.apply(this, args);
    };
    this.on(event, wrapper);
    return this;
  }

  emit(event, ...args) {
    const handlers = this.#listeners.get(event);
    if (!handlers || handlers.size === 0) return false;
    // Snapshot before iterating: a handler unsubscribing mid-emit shouldn't
    // affect this emit's iteration.
    [...handlers].forEach((handler) => handler.apply(this, args));
    return true;
  }
}
