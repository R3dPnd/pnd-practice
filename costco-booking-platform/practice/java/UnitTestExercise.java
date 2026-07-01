import java.util.List;
import java.util.Optional;

/**
 * UNIT TESTING EXERCISE — OrderService
 *
 * This file contains:
 *   1. The domain classes (Item, Order, OrderNotFoundException)
 *   2. The repository and email service interfaces to mock
 *   3. The OrderService class under test
 *   4. A blank OrderServiceTest class — YOUR JOB is to write the 4 tests
 *
 * Setup (Maven):
 *   Add to pom.xml:
 *     <dependency>
 *       <groupId>org.junit.jupiter</groupId>
 *       <artifactId>junit-jupiter</artifactId>
 *       <version>5.10.0</version>
 *       <scope>test</scope>
 *     </dependency>
 *     <dependency>
 *       <groupId>org.mockito</groupId>
 *       <artifactId>mockito-junit-jupiter</artifactId>
 *       <version>5.5.0</version>
 *       <scope>test</scope>
 *     </dependency>
 *
 * Tests to write in OrderServiceTest:
 *   1. placeOrder() happy path — verify the order is saved and returned
 *   2. placeOrder() — verify email is sent with the correct userId and orderId
 *   3. getOrder() — when order exists, returns it
 *   4. getOrder() — when order does not exist, throws OrderNotFoundException
 *
 * Conceptual questions to answer out loud:
 *   - What is the difference between a mock and a stub?
 *   - What does @InjectMocks do?
 *   - What does verify() assert?
 *   - Name 3 things that make a unit test bad.
 */

// ---- Domain classes ----

class Item {
    private final String name;
    private final int quantity;
    public Item(String name, int quantity) { this.name = name; this.quantity = quantity; }
    public String getName() { return name; }
}

class Order {
    private Long id;
    private final Long userId;
    private final List<Item> items;
    public Order(Long userId, List<Item> items) { this.userId = userId; this.items = items; }
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getUserId() { return userId; }
}

class OrderNotFoundException extends RuntimeException {
    public OrderNotFoundException(Long id) { super("Order not found: " + id); }
}

// ---- Interfaces to mock ----

interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(Long id);
}

interface EmailService {
    void sendConfirmation(Long userId, Long orderId);
}

// ---- Class under test ----

class OrderService {
    private final OrderRepository repo;
    private final EmailService emailService;

    public OrderService(OrderRepository repo, EmailService emailService) {
        this.repo = repo;
        this.emailService = emailService;
    }

    public Order placeOrder(Long userId, List<Item> items) {
        Order order = new Order(userId, items);
        Order saved = repo.save(order);
        emailService.sendConfirmation(userId, saved.getId());
        return saved;
    }

    public Order getOrder(Long id) {
        return repo.findById(id)
            .orElseThrow(() -> new OrderNotFoundException(id));
    }
}

// ---- Your test class (move to src/test/java in a real project) ----

// import org.junit.jupiter.api.Test;
// import org.junit.jupiter.api.extension.ExtendWith;
// import org.mockito.InjectMocks;
// import org.mockito.Mock;
// import org.mockito.junit.jupiter.MockitoExtension;
// import static org.junit.jupiter.api.Assertions.*;
// import static org.mockito.Mockito.*;

// @ExtendWith(MockitoExtension.class)
// class OrderServiceTest {
//
//     @Mock
//     private OrderRepository repo;
//
//     @Mock
//     private EmailService emailService;
//
//     @InjectMocks
//     private OrderService orderService;
//
//     // TODO — Test 1: placeOrder happy path
//     // Arrange: when repo.save() is called, return a saved order with id=99
//     // Act: call orderService.placeOrder(1L, items)
//     // Assert: result is not null, result.getId() == 99
//     //         verify repo.save() was called exactly once
//
//     // TODO — Test 2: placeOrder sends correct email
//     // Same setup as Test 1
//     // Assert: verify emailService.sendConfirmation(1L, 99L) was called once
//
//     // TODO — Test 3: getOrder returns order when found
//     // Arrange: when repo.findById(42L), return Optional.of(order)
//     // Act: call orderService.getOrder(42L)
//     // Assert: result.getId() == 42
//
//     // TODO — Test 4: getOrder throws when not found
//     // Arrange: when repo.findById(999L), return Optional.empty()
//     // Act + Assert: assertThrows(OrderNotFoundException.class, () -> orderService.getOrder(999L))
// }

public class UnitTestExercise {
    public static void main(String[] args) {
        System.out.println("This file is for unit test practice.");
        System.out.println("Implement the test stubs in the OrderServiceTest class above.");
        System.out.println("See JavaSolutions.java comments or README for the full solution.");
    }
}
