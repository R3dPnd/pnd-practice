import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * Practice: producer/consumer ad-event pipeline. See README.md.
 */
public class Practice {

    static class EventPipeline {
        EventPipeline(int capacity) {
            // TODO: set up a bounded queue and start a background consumer thread
        }

        void submit(String event) throws InterruptedException {
            // TODO: block if the queue is full; never drop an event
            throw new UnsupportedOperationException("not implemented");
        }

        List<String> shutdownAndDrain() throws InterruptedException {
            // TODO: signal shutdown, wait for the consumer to finish all queued work
            // (in order), return the processed events
            throw new UnsupportedOperationException("not implemented");
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
