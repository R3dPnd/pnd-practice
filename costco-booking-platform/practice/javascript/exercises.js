/**
 * INTERVIEW PRACTICE — JavaScript & jQuery Exercises
 *
 * Instructions:
 *   - Implement each function stub below.
 *   - Run in browser DevTools console or Node.js.
 *   - jQuery exercises are marked — open html-css/exercise.html in a browser
 *     to run those (jQuery is loaded via CDN in that file).
 *   - Check solutions.js when done.
 */

// =============================================================================
// Exercise 1 — Closure Counter
// Write makeCounter() so that each returned function has its own independent count.
// Two counters must NOT share state.
//
// Expected:
//   const a = makeCounter();
//   const b = makeCounter();
//   a(); // 1
//   a(); // 2
//   b(); // 1  ← independent
//
// EXPLANATION:
//   A closure is a function that has access to variables from its outer scope,
//   even after that outer function has finished executing. Each call to makeCounter()
//   creates a new scope with its own `count` variable. The returned function
//   "closes over" that variable, keeping it alive and private.
//
//   When you call a() the first time, it increments count (0+1=1) and returns 1.
//   The count variable persists in memory between calls (closure magic).
//   When you call b(), it has its OWN separate count variable (starting fresh at 0).
//   This demonstrates that each closure instance has independent state.
// =============================================================================
function makeCounter() {
    let count = 0;

    return function() {
        count++;
        return count;
    };
}

// =============================================================================
// Exercise 2 — Flatten one level deep
// Flatten a nested array using reduce(), then again using flat().
//
// Expected: flatten([[1,2],[3,4],[5]]) → [1,2,3,4,5]
//
// EXPLANATION (reduce version):
//   reduce() combines all elements in an array into a single value by applying
//   a function that takes an accumulator and current element.
//
//   Breakdown:
//   - acc: the accumulator (starts as [])
//   - curr: current sub-array being processed
//   - acc.concat(curr): combines the current sub-array into the accumulator
//   - The spread operator (...) unpacks nested arrays: [...[1,2], ...[3,4]] = [1,2,3,4]
//
// EXPLANATION (flat version):
//   Array.flat() is a built-in method that flattens nested arrays.
//   flat(1) flattens 1 level deep. flat() with no args flattens all levels.
//   This is simpler but less educational about how to use reduce().
// =============================================================================
function flattenWithReduce(arr) {
    return arr.reduce((acc, curr) => acc.concat(curr), []);
}

function flattenWithFlat(arr) {
    return arr.flat();
}

// =============================================================================
// Exercise 3 — Debounce
// Return a function that only calls fn after `delay` ms have passed
// since the LAST time it was invoked. Each new call resets the timer.
//
// Use case: search input — only fire the API call after the user stops typing.
//
// EXPLANATION:
//   debounce() returns a new function that manages timing.
//   Each time the returned function is called, we:
//   1. Clear the previous timeout (if it exists) using clearTimeout()
//   2. Set a NEW timeout that will call fn() after `delay` milliseconds
//
//   The `timeoutId` variable is stored in a closure so it persists between calls.
//   When you type in a search box quickly, each keystroke calls this function.
//   - First keystroke: sets timeout to call fn in 500ms
//   - Second keystroke (before 500ms): clears the first timeout, sets a NEW one
//   - User stops typing: the timeout finally runs after 500ms of silence
//
//   Without debounce, every keystroke would fire immediately (bad for performance).
// =============================================================================
function debounce(fn, delay) {
    let timeoutId = null;

    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            fn(...args);
        }, delay);
    };
}

// =============================================================================
// Exercise 4 — Promise chain
// Rewrite this callback-style code using async/await.
// Assume fetchUser(id) and fetchOrders(userId) both return Promises.
//
// Original callback version:
//   fetchUser(1, function(user) {
//     fetchOrders(user.id, function(orders) {
//       console.log(orders);
//     });
//   });
//
// EXPLANATION:
//   async/await is syntactic sugar over Promises.
//   - async function always returns a Promise
//   - await pauses execution until the Promise resolves
//   - It reads top-to-bottom (imperative), easier than nested .then() chains
//
//   Step by step:
//   1. const user = await fetchUser(userId)  — wait for the promise to resolve
//   2. const orders = await fetchOrders(user.id)  — then wait for this promise
//   3. return orders  — the function returns a promise that resolves to orders
//
//   Advantages over callbacks:
//   - No callback hell (pyramid of doom)
//   - Error handling with try/catch (instead of nested error callbacks)
//   - Looks like synchronous code but is non-blocking
// =============================================================================
async function getUserOrders(userId) {
    const user = await fetchUser(userId);
    const orders = await fetchOrders(user.id);
    return orders;
}

// =============================================================================
// Exercise 5 — this binding
// What does each console.log print? Write your answer as a comment.
// Then explain WHY.
//
// EXPLANATION:
//   `this` in JavaScript depends on HOW a function is called (not where it's defined).
//
//   Regular function (greetRegular):
//   - When called as obj.greetRegular(), `this` refers to the object (obj)
//   - So this.name = 'Dann'
//   - PRINTS: "Regular: Dann"
//   - WHY: Methods called on an object receive that object as `this`
//
//   Arrow function (greetArrow):
//   - Arrow functions DO NOT have their own `this`
//   - They inherit `this` from the enclosing scope (lexical binding)
//   - The enclosing scope is the module/global scope, where `this` is undefined (or window in browsers)
//   - this.name is undefined, so it prints undefined
//   - PRINTS: "Arrow: undefined"
//   - WHY: Arrow functions use lexical this (from outer scope), not dynamic this
//
//   KEY DIFFERENCE:
//   - Regular functions: get `this` from how they're called (dynamic)
//   - Arrow functions: get `this` from where they're defined (lexical)
// =============================================================================
const obj = {
    name: 'Dann',
    greetRegular: function() {
        console.log('Regular:', this.name);
    },
    greetArrow: () => {
        console.log('Arrow:', this.name);
    }
};

// obj.greetRegular(); // prints: "Regular: Dann" — WHY: method called on obj, so this=obj
// obj.greetArrow();   // prints: "Arrow: undefined" — WHY: arrow inherits this from global scope

// =============================================================================
// Exercise 6 — Array methods
// Without using a for-loop, compute:
//   a) The sum of all numbers in the array
//   b) All numbers greater than 3, doubled
//
// Input: [1, 2, 3, 4, 5, 6]
// Expected a: 21
// Expected b: [8, 10, 12]
//
// EXPLANATION (sum with reduce):
//   reduce(callback, initialValue):
//   - Takes a callback that receives (accumulator, current)
//   - initialValue (0): what acc starts as on first iteration
//   - Each iteration: acc += current, building up the sum
//   - Returns the final accumulated value
//
//   Walkthrough:
//   - acc=0, curr=1 → acc=0+1=1
//   - acc=1, curr=2 → acc=1+2=3
//   - acc=3, curr=3 → acc=3+3=6
//   - ... continues ... → final result = 21
//
// EXPLANATION (filter + map):
//   filter(predicate): returns new array with only elements where predicate is true
//   - [1,2,3,4,5,6].filter(n => n > 3) → [4, 5, 6]
//
//   map(transform): applies transform function to each element
//   - [4,5,6].map(n => n * 2) → [8, 10, 12]
//
//   Chained together:
//   - Start with [1,2,3,4,5,6]
//   - Filter keeps only [4,5,6]
//   - Map doubles each: [8,10,12]
// =============================================================================
const numbers = [1, 2, 3, 4, 5, 6];

const sum = numbers.reduce((acc, curr) => acc + curr, 0);
const filteredDoubled = numbers.filter(n => n > 3).map(n => n * 2);

// =============================================================================
// SECTION 2 — jQuery (run in html-css/exercise.html — jQuery must be loaded)
// =============================================================================

// =============================================================================
// jQuery Exercise 1
// On document ready:
//   - Hide all elements with class .alert
//   - Show them one at a time with a 500ms delay between each
//
// EXPLANATION:
//   $(document).ready() ensures the DOM is fully loaded before running code.
//   This is critical because jQuery needs elements to exist before manipulating them.
//
//   .find('.alert'): searches for all .alert elements within the document
//   .hide(): instantly hides them (CSS display: none)
//   .each(function(index) { ... }): iterates over each .alert element
//     - index: 0 for first, 1 for second, etc.
//     - $(this): refers to current element in the loop
//     - setTimeout(delay * index): schedules the show() call
//       * First alert (index 0): setTimeout(0) = show immediately
//       * Second alert (index 1): setTimeout(500) = show after 500ms
//       * Third alert (index 2): setTimeout(1000) = show after 1000ms
//   .show(): makes the element visible with animation
//
//   This creates a staggered reveal effect.
// =============================================================================
// $(document).ready(function() {
//     $(".alert").hide();
//     $(".alert").each(function(index) {
//         setTimeout(() => {
//             $(this).show();
//         }, 500 * index);
//     });
// });

// =============================================================================
// jQuery Exercise 2 — AJAX form submit
// When #login-form is submitted:
//   - Prevent default browser submission
//   - Read the value from input#username
//   - POST { username } as JSON to /api/login
//   - On success: show #welcome with response.message, hide #error
//   - On failure: show #error with "Login failed", hide #welcome
//
// EXPLANATION:
//   $('selector').on('event', callback): attaches an event handler
//   - 'submit': fires when form is submitted (by button or Enter key)
//   - callback(e): e is the event object
//
//   e.preventDefault(): stops the browser's default form submission behavior
//   - Without this, the page would reload (like traditional HTML form)
//
//   $('#username').val(): gets the value typed into that input
//
//   $.ajax({...}): sends an HTTP request
//   - type: 'POST' = HTTP method (could be 'GET', 'PUT', etc.)
//   - url: '/api/login' = endpoint to hit
//   - contentType: 'application/json' = server expects JSON
//   - data: JSON.stringify({username: ...}) = body of request (must be JSON string)
//   - success: function(response) = called if server responds with 200-299 status
//   - error: function() = called if server responds with 4xx/5xx or network fails
//
//   .show()/.hide(): make elements visible/invisible
//   .text(str): set the text content of an element
// =============================================================================
// $('#login-form').on('submit', function(e) {
//     e.preventDefault();
//
//     const username = $('#username').val();
//
//     $.ajax({
//         type: 'POST',
//         url: '/api/login',
//         contentType: 'application/json',
//         data: JSON.stringify({ username: username }),
//         success: function(response) {
//             $('#welcome').text(response.message).show();
//             $('#error').hide();
//         },
//         error: function() {
//             $('#error').text('Login failed').show();
//             $('#welcome').hide();
//         }
//     });
// });

// =============================================================================
// jQuery Exercise 3 — Event delegation
// Clicking a button with class .remove-btn should remove its parent <li>.
// Use event delegation on the <ul> so it works for dynamically added items too.
// (Direct binding with .click() will NOT work for dynamic items — explain why.)
//
// EXPLANATION:
//   Event delegation: attach handler to a parent element that will exist on page load.
//   The parent "catches" events bubbling up from its children.
//
//   WHY direct binding doesn't work for dynamic items:
//     When you do: $('.remove-btn').click(function() { ... })
//     jQuery finds all .remove-btn elements AT THAT MOMENT and attaches listeners.
//     If new .remove-btn buttons are added later (via AJAX, DOM manipulation),
//     they DON'T have listeners attached — they didn't exist when you bound!
//
//   WHY delegation works:
//     When you do: $('#item-list').on('click', '.remove-btn', function() { ... })
//     jQuery attaches ONE listener to #item-list (which exists when page loads).
//     Every time ANY click happens inside #item-list:
//       1. jQuery checks if the clicked element matches '.remove-btn'
//       2. If it does, it calls the handler
//     Since #item-list exists from the start, this works for future .remove-btn elements too!
//
//   $(this).parent(): gets the immediate parent of current element
//   .remove(): deletes the element from the DOM
//
//   The selector '#item-list' is the static parent (must exist at page load).
//   The selector '.remove-btn' is the dynamic child (can be added anytime).
// =============================================================================
// $('#item-list').on('click', '.remove-btn', function() {
//     $(this).parent().remove();
// });

// =============================================================================
// Quick-check runner (Node.js / browser console)
// =============================================================================
(function runChecks() {
    // Exercise 1
    const a = makeCounter(), b = makeCounter();
    console.assert(a() === 1, 'counter a: first call should return 1');
    console.assert(a() === 2, 'counter a: second call should return 2');
    console.assert(b() === 1, 'counter b: should be independent');

    // Exercise 2
    const nested = [[1,2],[3,4],[5]];
    console.assert(JSON.stringify(flattenWithReduce(nested)) === '[1,2,3,4,5]', 'flattenWithReduce');
    console.assert(JSON.stringify(flattenWithFlat(nested))   === '[1,2,3,4,5]', 'flattenWithFlat');

    // Exercise 6
    console.assert(sum === 21,                                   'sum of numbers');
    console.assert(JSON.stringify(filteredDoubled) === '[8,10,12]', 'filteredDoubled');

    console.log('All checks passed!');
})();
