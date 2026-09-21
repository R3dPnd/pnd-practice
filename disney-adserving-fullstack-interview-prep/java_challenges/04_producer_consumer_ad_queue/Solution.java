import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Solution {

    static class EventPipeline {
        private static final String POISON_PILL = "__SHUTDOWN__";
        private final BlockingQueue<String> queue;
        private final List<String> processed = new ArrayList<>();
        private final Thread consumerThread;

        EventPipeline(int capacity) {
            this.queue = new ArrayBlockingQueue<>(capacity);
            this.consumerThread = new Thread(this::consumeLoop);
            this.consumerThread.start();
        }

        void submit(String event) throws InterruptedException {
            queue.put(event); // blocks (backpressure) if the queue is full, never drops
        }

        private void consumeLoop() {
            try {
                while (true) {
                    String event = queue.take();
                    if (POISON_PILL.equals(event)) {
                        break;
                    }
                    synchronized (processed) {
                        processed.add(event); // stand-in for real processing work
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        List<String> shutdownAndDrain() throws InterruptedException {
            queue.put(POISON_PILL); // processed strictly after every real event ahead of it
            consumerThread.join();  // wait for the consumer to actually finish
            synchronized (processed) {
                return new ArrayList<>(processed);
            }
        }
    }

    public static void main(String[] args) throws InterruptedException {
        EventPipeline pipeline = new EventPipeline(5);
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 20; i++) {
                    pipeline.submit("event-" + i);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        producer.start();
        producer.join();

        List<String> processed = pipeline.shutdownAndDrain();
        List<String> expected = IntStream.range(0, 20)
                .mapToObj(i -> "event-" + i)
                .collect(Collectors.toList());

        System.out.println("processed count (expect 20): " + processed.size());
        System.out.println("processed in submission order (expect true): " + processed.equals(expected));
    }
}
