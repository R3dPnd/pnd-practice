import java.util.concurrent.CountDownLatch;

/**
 * Practice: concurrent, idempotent impression counter. See README.md.
 */
public class Practice {

    static class ImpressionCounter {

        boolean record(String campaignId, String impressionId) {
            // TODO: atomically dedupe by impressionId, then increment the
            // campaign's count only for genuinely new impressions.
            throw new UnsupportedOperationException("not implemented");
        }

        long getCount(String campaignId) {
            // TODO
            throw new UnsupportedOperationException("not implemented");
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ImpressionCounter counter = new ImpressionCounter();
        counter.record("campaignA", "imp-1");
        counter.record("campaignA", "imp-1"); // duplicate, same-thread
        counter.record("campaignA", "imp-2");
        System.out.println("single-threaded count (expect 2): " + counter.getCount("campaignA"));

        // 100 threads race to record the SAME impressionId concurrently
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

        // 200 threads each record a DISTINCT impressionId concurrently
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
