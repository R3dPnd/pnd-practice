package com.disneyprep.addecisioning.service;

import com.disneyprep.addecisioning.exception.AdNotEligibleException;
import com.disneyprep.addecisioning.model.AdCandidate;
import com.disneyprep.addecisioning.repository.AdCandidateRepository;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.List;
import java.util.Optional;

/**
 * The eligibility-filter-then-rank algorithm from
 * ../../../../../../java_challenges/05_ad_qualification_selection/, now sitting behind
 * a real Spring Boot service + REST layer. See
 * ../../../../../../system_design/examples/01_ad_decisioning_service.md for the full
 * system this is a slice of.
 */
@Service
public class AdDecisionService {

    // Descending eCPM, ties broken by ascending id — same comparator as the
    // java_challenges/05 solution.
    private static final Comparator<AdCandidate> RANKING =
            Comparator.comparingDouble(AdCandidate::eCpm).reversed()
                    .thenComparing(AdCandidate::id);

    private final AdCandidateRepository repository;
    private final Timer decisionTimer;
    private final Counter fallbackServedCounter;

    public AdDecisionService(AdCandidateRepository repository, MeterRegistry registry) {
        this.repository = repository;
        this.decisionTimer = Timer.builder("ad.decision.latency")
                .publishPercentiles(0.5, 0.95, 0.99)
                .register(registry);
        this.fallbackServedCounter = Counter.builder("ad.decision.fallback_served")
                .register(registry);
    }

    public AdCandidate decide(String sessionId, String contentId) {
        return decisionTimer.record(() -> {
            Optional<AdCandidate> best = repository.findAll().stream()
                    .filter(AdCandidate::isEligible)
                    .min(RANKING);

            if (best.isEmpty()) {
                fallbackServedCounter.increment();
                throw new AdNotEligibleException(
                        "No eligible ad candidate for session=" + sessionId + " content=" + contentId);
            }
            return best.get();
        });
    }

    public List<AdCandidate> rankEligible() {
        return repository.findAll().stream()
                .filter(AdCandidate::isEligible)
                .sorted(RANKING)
                .toList();
    }
}
