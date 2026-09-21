package com.disneyprep.addecisioning.service;

import com.disneyprep.addecisioning.exception.AdNotEligibleException;
import com.disneyprep.addecisioning.model.AdCandidate;
import com.disneyprep.addecisioning.repository.AdCandidateRepository;
import io.micrometer.core.instrument.simple.SimpleMeterRegistry;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.when;

/**
 * Plain Mockito unit test — no Spring context, fast. See spring_boot/notes.md Part 9.
 */
@ExtendWith(MockitoExtension.class)
class AdDecisionServiceTest {

    @Mock
    AdCandidateRepository repository;

    AdDecisionService service;

    @BeforeEach
    void setUp() {
        // Real (in-memory) MeterRegistry, not mocked: Timer.record()/Counter.increment()
        // need a concrete implementation to actually invoke the wrapped lambda.
        service = new AdDecisionService(repository, new SimpleMeterRegistry());
    }

    @Test
    void selectsHighestECpmEligibleCandidate_tieBrokenByIdAscending() {
        when(repository.findAll()).thenReturn(List.of(
                new AdCandidate("adA", "campaignA", "url-a", true, true, 4.50, 100.0),
                new AdCandidate("adB", "campaignB", "url-b", true, true, 6.20, 50.0),
                new AdCandidate("adC", "campaignC", "url-c", false, true, 9.99, 100.0), // fails targeting
                new AdCandidate("adD", "campaignD", "url-d", true, false, 8.00, 100.0), // not entitled
                new AdCandidate("adE", "campaignE", "url-e", true, true, 6.20, 0.0),    // no budget
                new AdCandidate("adF", "campaignF", "url-f", true, true, 6.20, 25.0)    // ties adB
        ));

        AdCandidate best = service.decide("session-1", "content-1");

        assertThat(best.id()).isEqualTo("adB");
    }

    @Test
    void rankEligible_returnsDescendingECpmWithIdTiebreak() {
        when(repository.findAll()).thenReturn(List.of(
                new AdCandidate("adA", "campaignA", "url-a", true, true, 4.50, 100.0),
                new AdCandidate("adB", "campaignB", "url-b", true, true, 6.20, 50.0),
                new AdCandidate("adF", "campaignF", "url-f", true, true, 6.20, 25.0)
        ));

        List<String> rankedIds = service.rankEligible().stream().map(AdCandidate::id).toList();

        assertThat(rankedIds).containsExactly("adB", "adF", "adA");
    }

    @Test
    void throwsAdNotEligibleException_whenNoCandidateQualifies() {
        when(repository.findAll()).thenReturn(List.of(
                new AdCandidate("adX", "campaignX", "url-x", false, true, 10.0, 10.0)
        ));

        assertThatThrownBy(() -> service.decide("session-1", "content-1"))
                .isInstanceOf(AdNotEligibleException.class);
    }
}
