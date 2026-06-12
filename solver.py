"""Deliberately-suboptimal IntentSolver for SN112 scoring-pipeline testing.

Subclasses the baseline AnvilSwapSolver. It always produces valid plans for the
first three generate_plan calls of a session (so it passes the Stage-3 smoke
test, which runs three synthetic intents in its own session), then solves only
every other intent during the longer benchmark session. The result: valid plans
on a subset, an aggregate score well below the champion, and a rich per-case
feedback report — without ever beating the champion.

Subnet-team test artifact: validates the submission scoring + feedback report
path on the live leader while champion adoption is disabled.
"""

from minotaur_subnet.sdk.solvers.anvil_swap_solver import AnvilSwapSolver
from minotaur_subnet.sdk.intent_solver import SolverMetadata


class SuboptimalSolver(AnvilSwapSolver):
    """Baseline router that intentionally skips half the benchmark intents."""

    def __init__(self) -> None:
        super().__init__()
        self._calls = 0

    def metadata(self) -> SolverMetadata:
        return SolverMetadata(
            name="suboptimal-test-solver",
            version="0.0.2",
            author="sn112-team-test",
        )

    def generate_plan(self, intent, state, snapshot=None):
        self._calls += 1
        # Always satisfy the Stage-3 smoke test (3 synthetic intents, own session).
        if self._calls <= 3:
            return super().generate_plan(intent, state, snapshot)
        # Benchmark session: solve only every other intent -> clearly suboptimal.
        if self._calls % 2 == 0:
            return None
        return super().generate_plan(intent, state, snapshot)


SOLVER_CLASS = SuboptimalSolver
