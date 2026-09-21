package com.disneyprep.addecisioning.controller;

import com.disneyprep.addecisioning.model.AdCandidate;
import com.disneyprep.addecisioning.service.AdDecisionService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/v1/ad-decision")
public class AdDecisionController {

    private final AdDecisionService adDecisionService;

    public AdDecisionController(AdDecisionService adDecisionService) {
        this.adDecisionService = adDecisionService;
    }

    @PostMapping
    public ResponseEntity<AdDecisionResponse> decide(@Valid @RequestBody AdDecisionRequest request) {
        AdCandidate candidate = adDecisionService.decide(request.sessionId(), request.contentId());
        return ResponseEntity.ok(AdDecisionResponse.from(candidate));
    }

    @GetMapping("/candidates")
    public List<AdDecisionResponse> rankedCandidates() {
        return adDecisionService.rankEligible().stream()
                .map(AdDecisionResponse::from)
                .toList();
    }
}
