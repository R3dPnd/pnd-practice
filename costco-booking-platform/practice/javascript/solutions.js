/**
 * SOLUTIONS — Do not open until you have attempted exercises.js
 */

// =============================================================================
// SECTION 1 — Core JavaScript
// =============================================================================

// Exercise 1 — Closure Counter
// The `count` variable lives in makeCounter's scope.
// Each call to makeCounter() creates a NEW closure with its own `count`.
function makeCounter() {
    let count = 0;
    return function() {
        return ++count;
    };
}

const a = makeCounter();
const b = makeCounter();
console.log(a()); // 1
console.log(a()); // 2
console.log(b()); // 1 — independent, has its own count


// Exercise 2 — Flatten
// reduce: accumulator starts as [], concat appends each inner array
function flattenWithReduce(arr) {
    return arr.reduce((acc, inner) => acc.concat(inner), []);
}

// flat() with no argument defaults to depth 1
function flattenWithFlat(arr) {
    return arr.flat();
}


// Exercise 3 — Debounce
// clearTimeout cancels any pending call each time the function is invoked.
// The actual fn() only runs after `delay` ms of silence.
function debounce(fn, delay) {
    let timer;
    return function(...args) {
        clearTimeout(timer);
        timer = setTimeout(() => fn.apply(this, args), delay);
    };
}

// Usage: attach to a search input
// const search = debounce(query => callAPI(query), 300);
// inputEl.addEventListener('input', e => search(e.target.value));


// Exercise 4 — async/await
// await unwraps the Promise — code reads top-to-bottom like synchronous code
async function getUserOrders(userId) {
    try {
        const user = await fetchUser(userId);
        const orders = await fetchOrders(user.id);
        console.log(orders);
        return orders;
    } catch (err) {
        console.error('Failed to load orders:', err);
        throw err;
    }
}


// Exercise 5 — this binding
// Regular function: `this` is determined at CALL TIME by how the function is called.
//   obj.greetRegular() → this = obj → prints "Dann"
//
// Arrow function: `this` is captured at DEFINITION TIME from the surrounding scope.
//   greetArrow is defined at the top level → this = window (or undefined in strict mode)
//   → prints undefined (not "Dann")
//
// KEY RULE: Arrow functions do NOT have their own `this`. Never use arrow functions
// as object methods when you need `this` to refer to the object.

const obj = {
    name: 'Dann',
    greetRegular: function() {
        console.log('Regular:', this.name); // "Dann"
    },
    greetArrow: () => {
        console.log('Arrow:', this.name);   // undefined
    }
};


// Exercise 6 — Array methods
const numbers = [1, 2, 3, 4, 5, 6];

const sum = numbers.reduce((acc, n) => acc + n, 0);  // 21

const filteredDoubled = numbers
    .filter(n => n > 3)   // [4, 5, 6]
    .map(n => n * 2);     // [8, 10, 12]


// =============================================================================
// SECTION 2 — jQuery
// =============================================================================

// jQuery Exercise 1 — Staggered show
$(document).ready(function() {
    $('.alert').hide();
    $('.alert').each(function(index) {
        $(this).delay(index * 500).fadeIn(300);
    });
});


// jQuery Exercise 2 — AJAX form submit
$('#login-form').on('submit', function(e) {
    e.preventDefault();
    const username = $('#username').val();

    $.ajax({
        url: '/api/login',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ username }),
        success: function(response) {
            $('#welcome').text(response.message).show();
            $('#error').hide();
        },
        error: function() {
            $('#error').text('Login failed').show();
            $('#welcome').hide();
        }
    });
});


// jQuery Exercise 3 — Event delegation
// Bind once on the parent #item-list, filter for clicks on .remove-btn.
// Works for dynamically added <li> elements because the event bubbles up
// to #item-list where the single handler lives.
$('#item-list').on('click', '.remove-btn', function() {
    $(this).closest('li').remove();
});

// WHY .click() fails for dynamic items:
// $('#item-list .remove-btn').click(...) binds only to elements that EXIST
// at bind time. New items added later have no handler. Delegation solves this
// by intercepting bubbled events at a stable parent element.


// =============================================================================
// Conceptual answers
// =============================================================================

// var vs let vs const
// var: function-scoped, hoisted (declared at top of function with value undefined)
// let: block-scoped, not accessible before declaration (temporal dead zone)
// const: block-scoped like let, but the binding cannot be reassigned
//   (the object it points to can still be mutated)

// What is hoisting?
// JavaScript moves var declarations to the top of their function scope at compile time.
// The DECLARATION is hoisted, not the initialization.
// console.log(x); var x = 5; → prints undefined (not ReferenceError)
// console.log(y); let y = 5; → throws ReferenceError

// Promise.all vs Promise.race
// Promise.all([p1, p2, p3]): waits for ALL to resolve; rejects if ANY rejects
// Promise.race([p1, p2, p3]): resolves/rejects as soon as the FIRST one settles

// == vs ===
// == allows type coercion: "5" == 5 → true, null == undefined → true
// === strict equality, no coercion: "5" === 5 → false
// Always use === in interviews unless you specifically need coercion.
