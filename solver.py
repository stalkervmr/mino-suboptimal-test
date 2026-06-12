"""Deliberately-suboptimal IntentSolver for SN112 scoring-pipeline testing.

Subclasses the baseline AnvilSwapSolver. Two adaptations let it run on the
public solver-base:v1 image and pass screening:

  * The function selector is precomputed (solver-base:v1 ships without a keccak
    hashing backend, so the baseline's keccak(...) call raises there).
  * initialize() falls back to placeholder addresses when none are configured,
    so the Stage-3 smoke test (which calls initialize({}) with no addresses)
    still gets structurally-valid plans.

Suboptimal by design: it always plans the first three calls of a session (the
Stage-3 smoke runs three synthetic intents in its own session) and then solves
only every other intent during the longer benchmark session, so the aggregate
score sits well below the champion while exercising the full per-case report.

Subnet-team test artifact (champion adoption disabled during the test window).
"""

import time

from eth_abi import encode as abi_encode

from minotaur_subnet.shared.types import ExecutionPlan, Interaction
from minotaur_subnet.v3.manifest import normalize_swap_intent_params
from minotaur_subnet.sdk.solvers.anvil_swap_solver import AnvilSwapSolver, _state_params
from minotaur_subnet.sdk.intent_solver import SolverMetadata

# keccak("swapExact(address,uint256,address)")[:4] — precomputed to avoid the
# keccak backend, which is absent from solver-base:v1.
_SWAP_EXACT_SELECTOR = bytes.fromhex("7c6b7c64")


class SuboptimalSolver(AnvilSwapSolver):
    def __init__(self) -> None:
        super().__init__()
        self._calls = 0

    def metadata(self) -> SolverMetadata:
        return SolverMetadata(
            name="suboptimal-test-solver",
            version="0.0.3",
            author="sn112-team-test",
        )

    def initialize(self, config) -> None:
        super().initialize(config)
        self.router = self.router or "0x0000000000000000000000000000000000000001"
        self.usdc = self.usdc or "0x0000000000000000000000000000000000000002"
        self.weth = self.weth or "0x0000000000000000000000000000000000000003"

    def generate_plan(self, intent, state, snapshot=None):
        self._calls += 1
        # Benchmark session: solve only every other intent after the Stage-3
        # smoke window (first 3 calls) -> clearly suboptimal aggregate.
        if self._calls > 3 and self._calls % 2 == 0:
            return None

        params = normalize_swap_intent_params(
            _state_params(state),
            receiver_default=state.contract_address or state.owner,
        )
        output_token = params.get("output_token", self.usdc) or self.usdc
        output_amount = params.get("min_output_amount", 0) or 1_800_000_000
        recipient = state.contract_address or state.owner
        args = abi_encode(
            ["address", "uint256", "address"],
            [output_token, output_amount, recipient],
        )
        calldata = "0x" + (_SWAP_EXACT_SELECTOR + args).hex()
        return ExecutionPlan(
            intent_id=intent.app_id,
            interactions=[
                Interaction(
                    target=self.router,
                    value="0",
                    call_data=calldata,
                    chain_id=state.chain_id,
                ),
            ],
            deadline=int(time.time()) + 300,
            nonce=state.nonce,
            metadata={"solver": "suboptimal-test"},
        )


SOLVER_CLASS = SuboptimalSolver
