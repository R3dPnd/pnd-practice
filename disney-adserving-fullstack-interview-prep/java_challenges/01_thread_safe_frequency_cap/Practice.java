import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Practice: thread-safe frequency cap. See README.md.
 * Implement FrequencyCap so tryRecord/currentCount are correct under concurrency
 * and evict least-recently-used keys once maxEntries is exceeded.
 */
public class Practice {

    static class FrequencyCap {
        private final int maxEntries;

        FrequencyCap(int maxEntries) {
            this.maxEntries = maxEntries;
            // TODO: initialize backing storage
        }

        boolean tryRecord(String key, int capPerWindow) {
            // TODO: atomically check-and-increment
            throw new UnsupportedOperationException("not implemented");
        }

        int currentCount(String key) {
            // TODO
            throw new UnsupportedOperationException("not implemented");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        FrequencyCap cap = new FrequencyCap(100);
        int allowed = 0;
        for (int i = 0; i < 5; i++) {
            if (cap.tryRecord("user1:campaignA", 3)) allowed++;
        }
        System.out.println("single-threaded allowed (expect 3): " + allowed);

        FrequencyCap cap2 = new FrequencyCap(100);
        int threads = 50;
        CountDownLatch latch = new CountDownLatch(threads);
        AtomicInteger allowedCount = new AtomicInteger();
        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                if (cap2.tryRecord("user2:campaignB", 10)) allowedCount.incrementAndGet();
                latch.countDown();
            }).start();
        }
        latch.await();
        System.out.println("concurrent allowed (expect exactly 10): " + allowedCount.get());

        FrequencyCap cap3 = new FrequencyCap(2);
        cap3.tryRecord("keyA", 5);
        cap3.tryRecord("keyB", 5);
        cap3.currentCount("keyA"); // touch keyA so it's most-recently-used
        cap3.tryRecord("keyC", 5); // should evict keyB (least recently used), not keyA
        System.out.println("keyB evicted (expect 0): " + cap3.currentCount("keyB"));
        System.out.println("keyA survived eviction (expect 1): " + cap3.currentCount("keyA"));
    }
}
