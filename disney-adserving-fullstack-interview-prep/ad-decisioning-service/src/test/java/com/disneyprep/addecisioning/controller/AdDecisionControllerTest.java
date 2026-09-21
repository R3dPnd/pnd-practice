package com.disneyprep.addecisioning.controller;

import com.disneyprep.addecisioning.model.AdCandidate;
import com.disneyprep.addecisioning.service.AdDecisionService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
 * Web-slice test: boots only the MVC layer, mocks the service. See
 * spring_boot/notes.md Part 9.
 */
@WebMvcTest(AdDecisionController.class)
class AdDecisionControllerTest {

    @Autowired
    MockMvc mockMvc;

    @MockBean
    AdDecisionService adDecisionService;

    @Test
    void returns400WhenSessionIdMissing() throws Exception {
        mockMvc.perform(post("/v1/ad-decision")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"contentId\":\"content-1\"}"))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("VALIDATION_FAILED"));
    }

    @Test
    void returns200WithDecision() throws Exception {
        when(adDecisionService.decide(any(), any()))
                .thenReturn(new AdCandidate("ad-1", "campaignA", "https://example.com/creative/a",
                        true, true, 6.20, 50.0));

        mockMvc.perform(post("/v1/ad-decision")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{\"sessionId\":\"s1\",\"contentId\":\"c1\"}"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.adId").value("ad-1"))
                .andExpect(jsonPath("$.campaignId").value("campaignA"));
    }
}
