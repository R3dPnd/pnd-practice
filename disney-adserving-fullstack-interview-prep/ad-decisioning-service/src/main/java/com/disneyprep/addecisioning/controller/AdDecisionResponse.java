package com.disneyprep.addecisioning.controller;

import com.disneyprep.addecisioning.model.AdCandidate;

public record AdDecisionResponse(String adId, String campaignId, String creativeUrl) {
    public static AdDecisionResponse from(AdCandidate candidate) {
        return new AdDecisionResponse(candidate.id(), candidate.campaignId(), candidate.creativeUrl());
    }
}
