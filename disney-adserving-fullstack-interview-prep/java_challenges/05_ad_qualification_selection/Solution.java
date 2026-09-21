import java.util.Comparator;
import java.util.List;
import java.util.Optional;

public class Solution {

    record AdCandidate(String id, boolean targetingMatch, boolean entitled,
                        double eCpm, double remainingBudget) {}

    private static boolean isEligible(AdCandidate c) {
        return c.targetingMatch() && c.entitled() && c.remainingBudget() > 0;
    }

    // Descending eCPM, ties broken by ascending id.
    private static final Comparator<AdCandidate> RANKING =
            Comparator.comparingDouble(AdCandidate::eCpm).reversed()
                    .thenComparing(AdCandidate::id);

    static Optional<AdCandidate> selectBestAd(List<AdCandidate> candidates) {
        return candidates.stream()
                .filter(Solution::isEligible)
                .min(RANKING); // "min" under this comparator == highest eCPM, smallest id on tie
    }

    static List<AdCandidate> rankEligible(List<AdCandidate> candidates) {
        return candidates.stream()
                .filter(Solution::isEligible)
                .sorted(RANKING)
                .toList();
    }

    public static void main(String[] args) {
        List<AdCandidate> candidates = List.of(
                new AdCandidate("adA", true, true, 4.50, 100.0),
                new AdCandidate("adB", true, true, 6.20, 50.0),
                new AdCandidate("adC", false, true, 9.99, 100.0),
                new AdCandidate("adD", true, false, 8.00, 100.0),
                new AdCandidate("adE", true, true, 6.20, 0.0),
                new AdCandidate("adF", true, true, 6.20, 25.0)
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
