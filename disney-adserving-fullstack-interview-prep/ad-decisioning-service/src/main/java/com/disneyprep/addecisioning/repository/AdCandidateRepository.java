package com.disneyprep.addecisioning.repository;

import com.disneyprep.addecisioning.model.AdCandidate;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * In-memory stand-in for the real candidate store (see
 * ../../../../../../spring_boot/notes.md Part 4 for what this looks like backed by
 * DynamoDB instead). Swapping the storage here for a real DynamoDbTable/JPA
 * repository shouldn't require any change to AdDecisionService, since the service
 * only depends on this interface's shape, not its implementation.
 */
@Repository
public class AdCandidateRepository {

    private final List<AdCandidate> seedCandidates = List.of(
            new AdCandidate("ad-1", "campaignA", "https://example.com/creative/a", true, true, 4.50, 100.0),
            new AdCandidate("ad-2", "campaignB", "https://example.com/creative/b", true, true, 6.20, 50.0),
            new AdCandidate("ad-3", "campaignC", "https://example.com/creative/c", false, true, 9.99, 100.0),
            new AdCandidate("ad-4", "campaignD", "https://example.com/creative/d", true, false, 8.00, 100.0),
            new AdCandidate("ad-5", "campaignE", "https://example.com/creative/e", true, true, 6.20, 0.0),
            new AdCandidate("ad-6", "campaignF", "https://example.com/creative/f", true, true, 6.20, 25.0)
    );

    public List<AdCandidate> findAll() {
        return seedCandidates;
    }
}
