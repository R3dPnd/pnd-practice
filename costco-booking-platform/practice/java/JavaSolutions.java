import java.util.*;
import java.util.stream.*;

/**
 * SOLUTIONS — Do not open until you have attempted JavaExercises.java
 */
public class JavaSolutions {

    // Exercise 1 — Reverse a String
    // Two-pointer approach: O(n/2) swaps, O(1) extra space.
    public static String reverse(String s) {
        char[] chars = s.toCharArray();
        int left = 0, right = chars.length - 1;
        while (left < right) {
            char temp = chars[left];
            chars[left] = chars[right];
            chars[right] = temp;
            left++;
            right--;
        }
        return new String(chars);
    }

    // Exercise 2 — FizzBuzz
    // Check % 15 first — if you check 3 and 5 independently you get both printed.
    public static void fizzBuzz() {
        for (int i = 1; i <= 100; i++) {
            if      (i % 15 == 0) System.out.println("FizzBuzz");
            else if (i % 3  == 0) System.out.println("Fizz");
            else if (i % 5  == 0) System.out.println("Buzz");
            else                  System.out.println(i);
        }
    }

    // Exercise 3 — Find Duplicates
    // HashSet.add() returns false when the element already exists — no second lookup needed.
    // LinkedHashSet preserves insertion order so the result matches input order.
    public static List<Integer> findDuplicates(List<Integer> input) {
        Set<Integer> seen = new HashSet<>();
        Set<Integer> duplicates = new LinkedHashSet<>();
        for (Integer n : input) {
            if (!seen.add(n)) {
                duplicates.add(n);
            }
        }
        return new ArrayList<>(duplicates);
    }

    // Exercise 4 — Word Frequency
    // getOrDefault(key, 0) avoids an explicit containsKey check.
    // LinkedHashMap preserves word insertion order.
    public static Map<String, Integer> wordFrequency(String sentence) {
        Map<String, Integer> freq = new LinkedHashMap<>();
        for (String word : sentence.split("\\s+")) {
            freq.put(word, freq.getOrDefault(word, 0) + 1);
        }
        return freq;
    }

    // Exercise 5a — Fibonacci recursive
    // O(2^n) time — recalculates the same subproblems. Fine for small n, terrible for n > 40.
    public static long fibRecursive(int n) {
        if (n <= 1) return n;
        return fibRecursive(n - 1) + fibRecursive(n - 2);
    }

    // Exercise 5b — Fibonacci iterative
    // O(n) time, O(1) space. Always prefer this in interviews.
    public static long fibIterative(int n) {
        if (n <= 1) return n;
        long prev = 0, curr = 1;
        for (int i = 2; i <= n; i++) {
            long next = prev + curr;
            prev = curr;
            curr = next;
        }
        return curr;
    }

    // Exercise 6 — First Non-Repeated Character
    // LinkedHashMap is critical — it preserves insertion order so we find the FIRST
    // character with count 1, not just any character with count 1.
    public static char firstNonRepeated(String s) {
        Map<Character, Integer> freq = new LinkedHashMap<>();
        for (char c : s.toCharArray()) {
            freq.put(c, freq.getOrDefault(c, 0) + 1);
        }
        for (Map.Entry<Character, Integer> entry : freq.entrySet()) {
            if (entry.getValue() == 1) return entry.getKey();
        }
        return '\0';
    }

    // Exercise 7 — Sum of Evens (Streams)
    public static int sumOfEvens(List<Integer> numbers) {
        return numbers.stream()
            .filter(n -> n % 2 == 0)
            .mapToInt(Integer::intValue)
            .sum();
    }

    // Exercise 8 — Filter and Transform (Streams)
    // Method reference String::toUpperCase is equivalent to name -> name.toUpperCase()
    public static List<String> filterNames(List<String> names) {
        return names.stream()
            .filter(name -> name.startsWith("A"))
            .map(String::toUpperCase)
            .sorted()
            .collect(Collectors.toList());
    }

    public static void main(String[] args) {
        System.out.println(reverse("hello"));
        System.out.println(findDuplicates(List.of(1, 2, 3, 2, 4, 3, 5)));
        System.out.println(wordFrequency("the cat sat on the mat the cat"));
        System.out.println(fibIterative(10));
        System.out.println(firstNonRepeated("aabbcdeef"));
        System.out.println(sumOfEvens(List.of(1, 2, 3, 4, 5, 6)));
        System.out.println(filterNames(List.of("Alice", "Bob", "Charlie", "Anna", "Brian")));
    }
}
