import java.util.List;
import java.util.Optional;

/**
 * Practice: ad qualification & selection. See README.md.
 */
public class Practice {

    record AdCandidate(String id, boolean targetingMatch, boolean entitled,
                        double eCpm, double remainingBudget) {}

    static Optional<AdCandidate> selectBestAd(List<AdCandidate> candidates) {
        // TODO: filter to eligible candidates, return the highest-eCPM one
        // (ties broken by id ascending), Optional.empty() if none eligible.
        throw new UnsupportedOperationException("not implemented");
    }

    static List<AdCandidate> rankEligible(List<AdCandidate> candidates) {
        // TODO: filter to eligible candidates, sorted highest-eCPM first,
        // ties broken by id ascending.
        throw new UnsupportedOperationException("not implemented");
    }

    public static void main(String[] args) {
        List<AdCandidate> candidates = List.of(
                new AdCandidate("adA", true, true, 4.50, 100.0),
                new AdCandidate("adB", true, true, 6.20, 50.0),
                new AdCandidate("adC", false, true, 9.99, 100.0),   // fails targeting
                new AdCandidate("adD", true, false, 8.00, 100.0),   // not entitled
                new AdCandidate("adE", true, true, 6.20, 0.0),      // no budget left
                new AdCandidate("adF", true, true, 6.20, 25.0)      // ties adB on eCPM
        );

        Optional<AdCandidate> best = selectBestAd(candidates);
        System.out.println("best ad id (expect adB, ties broken by id ascending): "
                + best.map(AdCandidate::id).orElse("<none>"));

        List<AdCandidate> ranked = rankEligible(candidates);
        System.out.println("ranked eligible ids (expect [adB, adF, adA]): "
                + ranked.stream().map(AdCandidate::id).toList());

        Optional<AdCandidate> none = selectBestAd(List.of(
                new AdCandidate("adX", false, true, 10.0, 10.0)
        ));
        System.out.println("no eligible candidates (expect <none>): "
                + none.map(AdCandidate::id).orElse("<none>"));
    }
}
