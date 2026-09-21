import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Practice: token bucket pacer. See README.md.
 */
public class Practice {

    static class TokenBucket {
        TokenBucket(double capacity, double refillPerSecond) {
            // TODO
        }

        boolean tryConsume(double tokens) {
            // TODO: lazily refill based on elapsed time (capped at capacity),
            // then atomically consume if enough tokens are available.
            throw new UnsupportedOperationException("not implemented");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        // no refill: exactly `capacity` units are consumable total, even under a race
        TokenBucket bucket = new TokenBucket(10, 0);
        int threads = 100;
        CountDownLatch latch = new CountDownLatch(threads);
        AtomicInteger successCount = new AtomicInteger();
        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                if (bucket.tryConsume(1)) successCount.incrementAndGet();
                latch.countDown();
            }).start();
        }
        latch.await();
        System.out.println("consumed under race (expect exactly 10): " + successCount.get());

        // refill behavior: capacity 5, refill 5 tokens/sec
        TokenBucket bucket2 = new TokenBucket(5, 5);
        int firstBurst = 0;
        for (int i = 0; i < 10; i++) if (bucket2.tryConsume(1)) firstBurst++;
        System.out.println("first burst consumed (expect 5, bucket starts full): " + firstBurst);

        Thread.sleep(1100); // allow ~5 tokens to refill
        int afterRefill = 0;
        for (int i = 0; i < 10; i++) if (bucket2.tryConsume(1)) afterRefill++;
        System.out.println("after ~1s refill (expect 5, capped at capacity): " + afterRefill);
    }
}
