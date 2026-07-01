import java.util.*;
import java.util.stream.*;

/**
 * INTERVIEW PRACTICE — Java Coding Exercises
 *
 * Instructions:
 *   - Implement each method stub below.
 *   - Do NOT look at JavaSolutions.java until you have a working attempt.
 *   - Run main() to check your output against the expected results.
 */
public class JavaExercises {

    // -------------------------------------------------------------------------
    // Exercise 1 — Reverse a String
    // Reverse the input string WITHOUT using StringBuilder.reverse().
    // Expected: reverse("hello") → "olleh"
    // -------------------------------------------------------------------------
    public static String reverse(String s) {
        StringBuilder sb = new StringBuilder();
        for (int i = s.length() - 1; i >= 0; i--) {
            sb.append(s.charAt(i));
        }
        return sb.toString();
    }

    // -------------------------------------------------------------------------
    // Exercise 2 — FizzBuzz
    // Print 1–100. Multiples of 3 → "Fizz", multiples of 5 → "Buzz",
    // multiples of both → "FizzBuzz".
    // -------------------------------------------------------------------------
    public static void fizzBuzz() {
        // TODO: implement — remember to check % 15 first
        for (int i = 1; i <= 100; i++) {
            if(i%15 == 0){
                System.out.println("FizzBuzz");
            } else if(i%3 == 0){
                System.out.println("Fizz");
            } else if(i%5 == 0){
                System.out.println("Buzz");
            } else {
                System.out.println(i);
            }
        }
    }

    // -------------------------------------------------------------------------
    // Exercise 3 — Find Duplicates
    // Return a list of values that appear more than once.
    // Each duplicate should appear only once in the result.
    // Expected: findDuplicates([1,2,3,2,4,3,5]) → [2, 3]
    // -------------------------------------------------------------------------
    public static List<Integer> findDuplicates(List<Integer> input) {
        // TODO: implement using a Set to track seen values
        List restult = new ArrayList<>();
        Set<Integer> set = new HashSet<>();
        for(Integer i : input){
            if(set.contains(i)){
                if(!restult.contains(i)){
                    restult.add(i);
                }
            } else {
                set.add(i);
            }
        }
        return restult;
    }

    // -------------------------------------------------------------------------
    // Exercise 4 — Word Frequency
    // Return a map of each word to the number of times it appears.
    // Expected: wordFrequency("the cat sat on the mat the cat")
    //           → {the=3, cat=2, sat=1, on=1, mat=1}
    // -------------------------------------------------------------------------
    public static Map<String, Integer> wordFrequency(String sentence) {
        Map<String, Integer> frequencyMap = new HashMap<>();
        String[] words = sentence.split(" ");
        for (String word : words) {
            frequencyMap.put(word, frequencyMap.getOrDefault(word, 0) + 1);
        }
        return frequencyMap;
    }

    // -------------------------------------------------------------------------
    // Exercise 5a — Fibonacci (recursive)
    // Return the nth Fibonacci number recursively.                                                                                         
    // Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21...
    // Expected: fib(7) → 13
    // -------------------------------------------------------------------------
    public static long fibRecursive(int n) {
        if(n == 0) return 0;
        if(n == 1) return 1;
        return fibRecursive(n - 1) + fibRecursive(n - 2);
    }

    // -------------------------------------------------------------------------
    // Exercise 5b — Fibonacci (iterative)
    // Return the nth Fibonacci number iteratively (preferred in interviews).
    // -------------------------------------------------------------------------
    public static long fibIterative(int n) {
        // TODO: implement — no recursion allowed
        if (n == 0) return 0;
        if (n == 1) return 1;
        long prev2 = 0;
        long prev1 = 1;
        for (int i = 2; i <= n; i++) {
            long current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        return prev1;
    }

    // -------------------------------------------------------------------------
    // Exercise 6 — First Non-Repeated Character
    // Return the first character in the string that does not repeat.
    // Expected: firstNonRepeated("aabbcdeef") → 'c'
    // Hint: what Map type preserves insertion order?
    // -------------------------------------------------------------------------
    public static char firstNonRepeated(String s) {
        // TODO: implement
            LinkedHashMap<Character, Integer> charCount = new LinkedHashMap<>();
            for (char c : s.toCharArray()) {
                charCount.put(c, charCount.getOrDefault(c, 0) + 1);
            }
            for (Map.Entry<Character, Integer> entry : charCount.entrySet()) {
                if (entry.getValue() == 1) {
                    return entry.getKey();
                }
            }
        return '\0';
    }

    // -------------------------------------------------------------------------
    // Exercise 7 — Sum of Evens (Streams)
    // Given a List<Integer>, use a Stream to return the sum of all even numbers.
    // Expected: sumOfEvens([1,2,3,4,5,6]) → 12
    // -------------------------------------------------------------------------
    public static int sumOfEvens(List<Integer> numbers) {
        int sum = 0;
        for(Integer i : numbers){
            if(i % 2 == 0){
                sum += i;
            }
        }
        return sum;
    }

    // -------------------------------------------------------------------------
    // Exercise 8 — Filter and Transform (Streams)
    // Given a list of names, return names starting with 'A',
    // uppercased and sorted alphabetically.
    // Expected: filterNames(["Alice","Bob","Charlie","Anna","Brian"])
    //           → ["ALICE", "ANNA"]
    // -------------------------------------------------------------------------
    public static List<String> filterNames(List<String> names) {
        // TODO: implement using stream().filter().map().sorted().collect()
            return names.stream()
                    .filter(name -> name.startsWith("A"))
                    .map(String::toUpperCase)
                    .sorted()
                    .collect(Collectors.toList());
    }

    // -------------------------------------------------------------------------
    // main() — run this to verify your answers
    // -------------------------------------------------------------------------
    public static void main(String[] args) {
        System.out.println("=== Exercise 1: Reverse ===");
        System.out.println(reverse("hello"));         // olleh
        System.out.println(reverse("java"));          // avaj
        System.out.println(reverse("a"));             // a

        System.out.println("\n=== Exercise 2: FizzBuzz ===");
        fizzBuzz();

        System.out.println("\n=== Exercise 3: Duplicates ===");
        System.out.println(findDuplicates(List.of(1, 2, 3, 2, 4, 3, 5)));  // [2, 3]
        System.out.println(findDuplicates(List.of(1, 1, 1)));               // [1]
        System.out.println(findDuplicates(List.of(1, 2, 3)));               // []

        System.out.println("\n=== Exercise 4: Word Frequency ===");
        System.out.println(wordFrequency("the cat sat on the mat the cat"));
        // {the=3, cat=2, sat=1, on=1, mat=1}

        System.out.println("\n=== Exercise 5: Fibonacci ===");
        System.out.println(fibRecursive(7));   // 13
        System.out.println(fibIterative(7));   // 13
        System.out.println(fibIterative(10));  // 55

        System.out.println("\n=== Exercise 6: First Non-Repeated ===");
        System.out.println(firstNonRepeated("aabbcdeef"));  // c
        System.out.println(firstNonRepeated("aabb"));       // \0 (none found)

        System.out.println("\n=== Exercise 7: Sum of Evens ===");
        System.out.println(sumOfEvens(List.of(1, 2, 3, 4, 5, 6)));  // 12

        System.out.println("\n=== Exercise 8: Filter Names ===");
        System.out.println(filterNames(List.of("Alice", "Bob", "Charlie", "Anna", "Brian")));
        // [ALICE, ANNA]
    }
}
