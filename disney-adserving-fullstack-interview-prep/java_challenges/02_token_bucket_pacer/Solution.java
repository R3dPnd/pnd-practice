import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {

    static class TokenBucket {
        private final double capacity;
        private final double refillPerSecond;
        private double availableTokens;
        private long lastRefillNanos;

        TokenBucket(double capacity, double refillPerSecond) {
            this.capacity = capacity;
            this.refillPerSecond = refillPerSecond;
            this.availableTokens = capacity;
            this.lastRefillNanos = System.nanoTime();
        }

        synchronized boolean tryConsume(double tokens) {
            refill();
            if (availableTokens >= tokens) {
                availableTokens -= tokens;
                return true;
            }
            return false;
        }

        private void refill() {
            long now = System.nanoTime();
            double elapsedSeconds = (now - lastRefillNanos) / 1_000_000_000.0;
            if (elapsedSeconds <= 0) return;
            double refillAmount = elapsedSeconds * refillPerSecond;
            if (refillAmount > 0) {
                availableTokens = Math.min(capacity, availableTokens + refillAmount);
                lastRefillNanos = now;
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
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

        TokenBucket bucket2 = new TokenBucket(5, 5);
        int firstBurst = 0;
        for (int i = 0; i < 10; i++) if (bucket2.tryConsume(1)) firstBurst++;
        System.out.println("first burst consumed (expect 5, bucket starts full): " + firstBurst);

        Thread.sleep(1100);
        int afterRefill = 0;
        for (int i = 0; i < 10; i++) if (bucket2.tryConsume(1)) afterRefill++;
        System.out.println("after ~1s refill (expect 5, capped at capacity): " + afterRefill);
    }
}
