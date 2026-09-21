import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.atomic.AtomicLong;

public class Solution {

    static class ImpressionCounter {
        private final Set<String> seenImpressionIds = ConcurrentHashMap.newKeySet();
        private final ConcurrentHashMap<String, AtomicLong> countsByCampaign = new ConcurrentHashMap<>();

        boolean record(String campaignId, String impressionId) {
            boolean isNew = seenImpressionIds.add(impressionId); // atomic: only one caller sees true
            if (isNew) {
                countsByCampaign.computeIfAbsent(campaignId, id -> new AtomicLong()).incrementAndGet();
            }
            return isNew;
        }

        long getCount(String campaignId) {
            AtomicLong count = countsByCampaign.get(campaignId);
            return count == null ? 0 : count.get();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ImpressionCounter counter = new ImpressionCounter();
        counter.record("campaignA", "imp-1");
        counter.record("campaignA", "imp-1");
        counter.record("campaignA", "imp-2");
        System.out.println("single-threaded count (expect 2): " + counter.getCount("campaignA"));

        ImpressionCounter counter2 = new ImpressionCounter();
        int threads = 100;
        CountDownLatch latch = new CountDownLatch(threads);
        for (int i = 0; i < threads; i++) {
            new Thread(() -> {
                counter2.record("campaignB", "dup-imp");
                latch.countDown();
            }).start();
        }
        latch.await();
        System.out.println("concurrent duplicate record count (expect exactly 1): "
                + counter2.getCount("campaignB"));

        ImpressionCounter counter3 = new ImpressionCounter();
        int n = 200;
        CountDownLatch latch2 = new CountDownLatch(n);
        for (int i = 0; i < n; i++) {
            final int id = i;
            new Thread(() -> {
                counter3.record("campaignC", "imp-" + id);
                latch2.countDown();
            }).start();
        }
        latch2.await();
        System.out.println("concurrent distinct impressions (expect 200): "
                + counter3.getCount("campaignC"));

        System.out.println("unknown campaign count (expect 0): " + counter3.getCount("campaignZ"));
    }
}
