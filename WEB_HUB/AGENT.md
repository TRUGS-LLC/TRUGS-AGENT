# WEB_HUB — Agent Instructions

<trl>
DEFINE "WEB_HUB" AS DATA graph FOR RECORD web_resource.
EACH DATA node SHALL CONTAIN RECORD url AND RECORD purpose AND RECORD category.
EACH DATA edge SHALL CONTAIN RECORD weight FROM 0.0 TO 1.0.
AGENT SHALL READ DATA graph WEB_HUB TO NAVIGATE RECORD web_landscape.
</trl>

The WEB_HUB is a TRUG that indexes web resources — papers, repos, tools, articles, standards — organized into three branches that converge on TRUGS-AGENT.

## How to Read

<trl>
AGENT SHALL READ DATA graph web.trug.json TO UNDERSTAND RECORD landscape.
AGENT SHALL FOLLOW DATA edge WITH HIGH RECORD weight FIRST.
AGENT SHALL USE RECORD purpose TO DECIDE IF RESOURCE IS RELEVANT BEFORE FETCH.
AGENT SHALL_NOT FETCH RECORD url UNLESS RECORD purpose MATCHES RECORD task.
</trl>

## Three Branches

<trl>
DEFINE "structured_agent" AS STAGE — RECORD prompt_ambiguity MOTIVATES INTERFACE TRL.
DEFINE "graph_native" AS STAGE — RECORD graph_tooling MOTIVATES MODULE FOLDER AND PIPELINE TRUGGING.
DEFINE "agent_protocols" AS STAGE — RECORD agent_reliability MOTIVATES PIPELINE AAA AND MODULE MEMORY AND DATA EPIC.
EACH STAGE FEEDS RECORD trugs_agent_repo.
</trl>

## Updating the Hub

<trl>
IF AGENT DISCOVER RELEVANT RECORD web_resource THEN AGENT MAY ADD DATA node TO DATA graph.
EACH NEW DATA node SHALL CONTAIN RECORD url AND RECORD purpose AND RECORD category.
AGENT SHALL CREATE DATA edge WITH RECORD weight TO EXISTING DATA node.
AGENT SHALL VALIDATE DATA graph AFTER UPDATE.
</trl>
