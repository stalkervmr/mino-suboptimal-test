"""Deliberately-suboptimal IntentSolver for SN112 scoring-pipeline testing.

Subclasses the baseline AnvilSwapSolver but solves only every other intent,
so the aggregate benchmark score sits well below the champion. The solved
subset still produces valid plans, which exercises the full per-case feedback
report on GET /v1/submissions/{id}/status without ever beating the champion.

Subnet-team test artifact: used to validate the submission scoring + feedback
report path on the live leader while champion adoption is disabled.
"""

from minotaur_subnet.sdk.solvers.anvil_swap_solver import AnvilSwapSolver
from minotaur_subnet.sdk.intent_solver import SolverMetadata


class SuboptimalSolver(AnvilSwapSolver):
    """Baseline router that intentionally skips half the intents."""

    def __init__(self) -> None:
        super().__init__()
        self._calls = 0

    def metadata(self) -> SolverMetadata:
        return SolverMetadata(
            name="suboptimal-test-solver",
            version="0.0.1",
            author="sn112-team-test",
        )

    def generate_plan(self, intent, state, snapshot=None):
        # Suboptimal on purpose: solve only every other intent so the
        # aggregate score falls short of the champion's dethrone margin.
        self._calls += 1
        if self._calls % 2 == 0:
            return None
        return super().generate_plan(intent, state, snapshot)


SOLVER_CLASS = SuboptimalSolver
