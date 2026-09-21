import java.util.LinkedHashMap;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicInteger;

public class Solution {

    static class FrequencyCap {
        private final int maxEntries;
        private final Map<String, Integer> counts;

        FrequencyCap(int maxEntries) {
            this.maxEntries = maxEntries;
            // accessOrder=true reorders entries on get()/put() so the eldest entry
            // (per removeEldestEntry) is the least-recently-used one, not just the
            // least-recently-inserted one.
            this.counts = new LinkedHashMap<>(16, 0.75f, true) {
                @Override
                protected boolean removeEldestEntry(Map.Entry<String, Integer> eldest) {
                    return size() > FrequencyCap.this.maxEntries;
                }
            };
        }

        synchronized boolean tryRecord(String key, int capPerWindow) {
            Integer existing = counts.get(key); // get(), not getOrDefault: refreshes LRU order
            int current = existing == null ? 0 : existing;
            if (current >= capPerWindow) {
                return false;
            }
            counts.put(key, current + 1);
            return true;
        }

        synchronized int currentCount(String key) {
            Integer existing = counts.get(key);
            return existing == null ? 0 : existing;
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
