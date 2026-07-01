import java.util.List;

/**
 * OOP DESIGN EXERCISE — Shape Hierarchy
 *
 * Task:
 *   1. Create an abstract class Shape with an abstract method area().
 *   2. Implement Circle, Rectangle, and Triangle as subclasses.
 *   3. Implement totalArea(List<Shape>) that returns the sum of all areas.
 *   4. Override toString() on Shape to print: "Circle with area 78.54"
 *
 * Interviewer follow-up questions to be ready for:
 *   - Why abstract class instead of interface here?
 *   - What changes if two shapes share a common formula (e.g., area = base * height)?
 *   - How would you add a Polygon shape without changing existing code? (Open/Closed Principle)
 *
 * Uncomment the main() assertions once you have implemented the classes.
 */
public class OOPExercise {

    // TODO: define abstract class Shape here
    public abstract class Shape {
        public abstract double area();

        @Override
        public String toString() {
            return getClass().getSimpleName() + " with area " + String.format("%.2f", area());
        }
    }

    // TODO: define class Circle extends Shape
    public class Circle extends Shape {
        private final double radius;
        public Circle(double radius) { this.radius = radius; }

        @Override
        public double area() { return Math.PI * radius * radius; }
    }

    // TODO: define class Rectangle extends Shape
    public class Rectangle extends Shape {
        private final double width, height;
        public Rectangle(double width, double height) { this.width = width; this.height = height; }

        @Override
        public double area() { return width * height; }
    }

    // TODO: define class Triangle extends Shape
    public class Triangle extends Shape {
        private final double base, height;
        public Triangle(double base, double height) { this.base = base; this.height = height; }

        @Override
        public double area() { return 0.5 * base * height; }
    }

    // TODO: implement this method
    public static double totalArea(List<Shape> shapes) {
        return 0;
    }

    public static void main(String[] args) {
        // Uncomment after implementing:

        // Shape circle    = new Circle(5);
        // Shape rectangle = new Rectangle(4, 6);
        // Shape triangle  = new Triangle(3, 8);

        // System.out.println(circle);     // Circle with area 78.54
        // System.out.println(rectangle);  // Rectangle with area 24.00
        // System.out.println(triangle);   // Triangle with area 12.00

        // List<Shape> shapes = List.of(circle, rectangle, triangle);
        // System.out.printf("Total area: %.2f%n", totalArea(shapes)); // 114.54
    }
}

// ----------------------------- SOLUTION BELOW — scroll only after attempting ----
//
// abstract class Shape {
//     public abstract double area();
//
//     @Override
//     public String toString() {
//         return getClass().getSimpleName() + " with area " + String.format("%.2f", area());
//     }
// }
//
// class Circle extends Shape {
//     private final double radius;
//     public Circle(double radius) { this.radius = radius; }
//
//     @Override
//     public double area() { return Math.PI * radius * radius; }
// }
//
// class Rectangle extends Shape {
//     private final double width, height;
//     public Rectangle(double width, double height) { this.width = width; this.height = height; }
//
//     @Override
//     public double area() { return width * height; }
// }
//
// class Triangle extends Shape {
//     private final double base, height;
//     public Triangle(double base, double height) { this.base = base; this.height = height; }
//
//     @Override
//     public double area() { return 0.5 * base * height; }
// }
//
// public static double totalArea(List<Shape> shapes) {
//     return shapes.stream().mapToDouble(Shape::area).sum();
// }
