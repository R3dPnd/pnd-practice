package com.disneyprep.addecisioning.controller;

import jakarta.validation.constraints.NotBlank;

public record AdDecisionRequest(
        @NotBlank String sessionId,
        @NotBlank String contentId
) {
}
