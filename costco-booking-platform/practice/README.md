# Interview Practice — Costco Booking Platform

Practice files covering all topics for the technical interview.

## Folder Structure

```
practice/
├── java/
│   ├── JavaExercises.java        — 8 coding exercises (no solutions)
│   ├── JavaSolutions.java        — full solutions with explanations
│   ├── OOPExercise.java          — Shape hierarchy design exercise
│   └── UnitTestExercise.java     — OrderService + tests to write
├── sql/
│   ├── schema.sql                — tables + sample data to set up locally
│   ├── exercises.sql             — 6 queries to write (blanks)
│   └── solutions.sql             — full solutions with notes
├── javascript/
│   ├── exercises.js              — JS + jQuery exercises (blanks)
│   └── solutions.js              — full solutions with explanations
├── html-css/
│   ├── exercise.html             — layout to build from scratch
│   └── solution.html             — completed solution
└── rest/
    └── rest-quiz.md              — REST concepts Q&A + endpoint design
```

## How to Use

### Java
Open `java/JavaExercises.java` and implement each method stub.
Check your work against `java/JavaSolutions.java`.

Run with any Java IDE (IntelliJ, Eclipse, VS Code + Java extension) or:
```
javac JavaExercises.java && java JavaExercises
```

For unit tests, add JUnit 5 + Mockito to your classpath or use Maven/Gradle.

### SQL
1. Go to [SQLiteOnline.com](https://sqliteonline.com) (free, no install)
2. Paste and run `schema.sql` to create the tables and seed data
3. Write your answers in `exercises.sql`
4. Compare against `solutions.sql`

### JavaScript / jQuery
Open `javascript/exercises.js` in VS Code or paste into browser DevTools console.
For jQuery exercises, open `html-css/exercise.html` in a browser (jQuery is loaded via CDN).

### HTML/CSS
Open `html-css/exercise.html` in a browser and build the layout described in the comments.
Compare against `html-css/solution.html`.

## Priority Study Order

| Day | Focus |
|-----|-------|
| 1 | Java exercises — write all 8 from scratch |
| 2 | SQL queries — run against real DB |
| 3 | Unit tests — write all 4 tests from memory |
| 4 | JS/jQuery + REST quiz out loud |

## Interview Rounds

**Round 1** — Hiring Manager (Pragya Darbari): Resume, online test, Java knowledge basics

**Round 2** — Senior Developers: Java (primary), SQL, CSS/HTML, JavaScript, jQuery, REST, Unit Testing
