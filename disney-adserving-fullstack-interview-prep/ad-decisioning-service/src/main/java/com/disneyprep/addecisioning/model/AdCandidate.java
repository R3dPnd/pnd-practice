package com.disneyprep.addecisioning.model;

/**
 * A candidate ad for a given decision request. In a real system, targetingMatch
 * and entitled would come from evaluating campaign targeting rules and the user's
 * entitlement status; remainingBudget would come from the pacing service
 * (see ../../../../../../system_design/examples/04_ad_pacing_budget_service.md).
 * Here they're pre-seeded on the in-memory candidates for the skeleton.
 */
public record AdCandidate(
        String id,
        String campaignId,
        String creativeUrl,
        boolean targetingMatch,
        boolean entitled,
        double eCpm,
        double remainingBudget
) {
    public boolean isEligible() {
        return targetingMatch && entitled && remainingBudget > 0;
    }
}
