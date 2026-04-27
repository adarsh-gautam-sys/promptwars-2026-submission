"""
Unit tests for ElectionGuide AI tools.
Tests each FunctionTool to verify structured data output.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from election_agent.tools import (
    get_election_timeline,
    get_voter_registration_guide,
    get_nomination_process,
    get_polling_day_guide,
    get_counting_process,
    check_eligibility,
)


class TestElectionTimeline:
    def test_returns_dict(self):
        result = get_election_timeline()
        assert isinstance(result, dict)

    def test_has_stages(self):
        result = get_election_timeline()
        assert "stages" in result

    def test_has_nine_stages(self):
        result = get_election_timeline()
        assert len(result["stages"]) == 9

    def test_general_election_type(self):
        result = get_election_timeline(election_type="general")
        assert "Lok Sabha" in result["election_type"]

    def test_state_election_type(self):
        result = get_election_timeline(election_type="state")
        assert "State" in result["election_type"]


class TestVoterRegistration:
    def test_returns_dict(self):
        result = get_voter_registration_guide()
        assert isinstance(result, dict)

    def test_default_has_both_methods(self):
        result = get_voter_registration_guide()
        assert "online_steps" in result
        assert "offline_steps" in result

    def test_online_only(self):
        result = get_voter_registration_guide(method="online")
        assert "online_steps" in result
        assert "offline_steps" not in result

    def test_offline_only(self):
        result = get_voter_registration_guide(method="offline")
        assert "offline_steps" in result
        assert "online_steps" not in result

    def test_has_forms(self):
        result = get_voter_registration_guide()
        assert "forms" in result
        assert len(result["forms"]) >= 3


class TestNominationProcess:
    def test_returns_dict(self):
        result = get_nomination_process()
        assert isinstance(result, dict)

    def test_has_eligibility(self):
        result = get_nomination_process()
        assert "eligibility" in result

    def test_has_security_deposit(self):
        result = get_nomination_process()
        assert "security_deposit" in result


class TestPollingDayGuide:
    def test_returns_dict(self):
        result = get_polling_day_guide()
        assert isinstance(result, dict)

    def test_has_voting_steps(self):
        result = get_polling_day_guide()
        assert "voting_steps" in result
        assert len(result["voting_steps"]) >= 7

    def test_has_evm_info(self):
        result = get_polling_day_guide()
        assert "evm_info" in result


class TestCountingProcess:
    def test_returns_dict(self):
        result = get_counting_process()
        assert isinstance(result, dict)

    def test_has_counting_stages(self):
        result = get_counting_process()
        assert "counting_stages" in result
        assert len(result["counting_stages"]) >= 4


class TestCheckEligibility:
    def test_eligible_adult_citizen(self):
        result = check_eligibility(age=25, citizenship="indian")
        assert isinstance(result, dict)
        assert result["eligible"] is True

    def test_underage_not_eligible(self):
        result = check_eligibility(age=16, citizenship="indian")
        assert result["eligible"] is False

    def test_non_citizen_not_eligible(self):
        result = check_eligibility(age=30, citizenship="other")
        assert result["eligible"] is False

    def test_lok_sabha_candidate_eligible(self):
        result = check_eligibility(age=26, citizenship="indian", purpose="lok_sabha")
        assert result["eligible"] is True

    def test_lok_sabha_candidate_too_young(self):
        result = check_eligibility(age=23, citizenship="indian", purpose="lok_sabha")
        assert result["eligible"] is False

    def test_exactly_18(self):
        result = check_eligibility(age=18, citizenship="indian")
        assert result["eligible"] is True

    def test_exactly_17(self):
        result = check_eligibility(age=17, citizenship="indian")
        assert result["eligible"] is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
